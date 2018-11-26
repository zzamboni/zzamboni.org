+++
title = "My Emacs Configuration, With Commentary"
author = ["Diego Zamboni"]
summary = "I have enjoyed slowly converting my configuration files to literate programming style using org-mode in Emacs. It's now the turn of my Emacs configuration file."
date = 2017-12-17T20:14:00+01:00
tags = ["config", "howto", "literateprogramming", "literateconfig", "emacs"]
draft = false
creator = "Emacs 26.1 (Org mode 9.1.14 + ox-hugo)"
featured_image = "/images/emacs-logo.svg"
toc = true
+++

Last update: **November 27, 2018**

I have enjoyed slowly converting my configuration files to [literate programming](http://www.howardism.org/Technical/Emacs/literate-programming-tutorial.html) style style using org-mode in Emacs. I previously posted my [Elvish configuration](../my-elvish-configuration-with-commentary/), and now it's the turn of my Emacs configuration file. The text below is included directly from my [init.org](https://github.com/zzamboni/dot%5Femacs/blob/master/init.org) file. Please note that the text below is a snapshot as the file stands as of the date shown above, but it is always evolving. See the [init.org file in GitHub](https://github.com/zzamboni/dot%5Femacs/blob/master/init.org) for my current, live configuration, and the generated file at <https://github.com/zzamboni/dot%5Femacs/blob/master/init.el>.


## References {#references}

Emacs config is an art, and I have learned a lot by reading through other people's config files, and from many other resources. These are some of the best ones (several are also written in org mode). You will find snippets from all of these (and possibly others) throughout my config.

-   [Sacha Chua's Emacs Configuration](http://pages.sachachua.com/.emacs.d/Sacha.html)
-   [Uncle Dave's Emacs config](https://github.com/daedreth/UncleDavesEmacs#user-content-ido-and-why-i-started-using-helm)
-   [PythonNut's Emacs config](https://github.com/PythonNut/emacs-config)
-   [Mastering Emacs](https://www.masteringemacs.org/)


## Performance optimization {#performance-optimization}

Lately I've been playing with optimizing my Emacs load time. I have found a couple of useful resources, including:

-   [Two easy little known steps to speed up Emacs start up time](https://www.reddit.com/r/emacs/comments/3kqt6e/2%5Feasy%5Flittle%5Fknown%5Fsteps%5Fto%5Fspeed%5Fup%5Femacs%5Fstart/)
-   [Advanced Techniques for Reducing Emacs Startup Time](https://blog.d46.us/advanced-emacs-startup/)

Based on these, I have added the code below.

First, a hook that reports how long and how many garbage collections the startup took.

```emacs-lisp
;; Use a hook so the message doesn't get clobbered by other messages.
(add-hook 'emacs-startup-hook
          (lambda ()
            (message "Emacs ready in %s with %d garbage collections."
                     (format "%.2f seconds"
                             (float-time
                              (time-subtract after-init-time before-init-time)))
                     gcs-done)))
```

Next, we wrap the whole init file in a block that sets `file-name-handler-alist` to `nil` to prevent any special-filename parsing of files loaded from the init file (e.g. remote files loaded through tramp, etc.). The `let` block gets closed in the [Epilogue](#epilogue).

```emacs-lisp
(let ((file-name-handler-alist nil))
```

We set `gc-cons-threshold` to its maximum value, to prevent any garbage collection from happening during load time. We also reset this value in the [Epilogue](#epilogue).

```emacs-lisp
(setq gc-cons-threshold most-positive-fixnum)
```


## Customized variables {#customized-variables}

Emacs has its own [Customization mechanism](https://www.gnu.org/software/emacs/manual/html%5Fnode/emacs/Easy-Customization.html#Easy-Customization) for easily customizing many parameters. To make it easier to manage, I keep the customized variables and faces in a separate file and load it from the main file. A lot of my custom settings are configured from this init file as well, but there are always some which I change by hand for added flexibility.

```emacs-lisp
(setq custom-file "~/.emacs.d/custom.el")
(load custom-file)
```

Here is the current contents of my [custom.el](https://github.com/zzamboni/dot-emacs/blob/master/custom.el) file.

```emacs-lisp
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(ad-redefinition-action (quote accept))
 '(auto-insert-directory "~/.emacs.d/auto-insert/" nil nil "Customized with use-package autoinsert")
 '(backup-directory-alist (quote (("." . "~/.emacs.d/backups"))))
 '(cider-repl-history-file "~/.emacs.d/cider-history" t nil "Customized with use-package cider")
 '(cider-repl-history-size 5000 t nil "Customized with use-package cider")
 '(cider-repl-pop-to-buffer-on-connect t t nil "Customized with use-package cider")
 '(cider-repl-result-prefix "; => " t nil "Customized with use-package cider")
 '(cider-repl-use-clojure-font-lock t t nil "Customized with use-package cider")
 '(cider-repl-use-pretty-printing nil t nil "Customized with use-package cider")
 '(cider-repl-wrap-history t t nil "Customized with use-package cider")
 '(cider-show-error-buffer nil t nil "Customized with use-package cider")
 '(column-number-mode t)
 '(custom-safe-themes
   (quote
    ("e08cf6a643018ccf990a099bcf82903d64f02e64798d13a1859e79e47c45616e" "7f89ec3c988c398b88f7304a75ed225eaac64efa8df3638c815acc563dfd3b55" "cd4d1a0656fee24dc062b997f54d6f9b7da8f6dc8053ac858f15820f9a04a679" "c74e83f8aa4c78a121b52146eadb792c9facc5b1f02c917e3dbb454fca931223" "a27c00821ccfd5a78b01e4f35dc056706dd9ede09a8b90c6955ae6a390eb1c1e" "3c83b3676d796422704082049fc38b6966bcad960f896669dfc21a7a37a748fa" "6ac7c0f959f0d7853915012e78ff70150bfbe2a69a1b703c3ac4184f9ae3ae02" "8e4efc4bed89c4e67167fdabff77102abeb0b1c203953de1e6ab4d2e3a02939a" "a1a966cf2e87be6a148158c79863440ba2e45aa06cc214341feafe5c6deca4f2" "3eb2b5607b41ad8a6da75fe04d5f92a46d1b9a95a202e3f5369e2cdefb7aac5c" "3d0142352ce19c860047ad7402546944f84c270e84ae479beddbc2608268e0e5" "a33858123d3d3ca10c03c657693881b9f8810c9e242a62f1ad6380adf57b031c" "a40eac965142a2057269f8b2abd546b71a0e58e733c6668a62b1ad1aa7669220" "7be789f201ea16242dab84dd5f225a55370dbecae248d4251edbd286fe879cfa" "94dac4d15d12ba671f77a93d84ad9f799808714d4c5d247d5fd944df951b91d6" "4d8fab23f15347bce54eb7137789ab93007010fa47296c2f36757ff84b5b3c8a" default)))
 '(desktop-lazy-idle-delay 1 nil nil "Restore the rest of the buffers 1 seconds later")
 '(desktop-lazy-verbose nil nil nil "Be silent about lazily opening buffers")
 '(desktop-restore-eager 1 nil nil "Restore only the first buffer right away")
 '(easy-hugo-basedir "~/Personal/devel/zzamboni.org/zzamboni.org/" t nil "Customized with use-package easy-hugo")
 '(easy-hugo-previewtime "300" t nil "Customized with use-package easy-hugo")
 '(easy-hugo-url "http://zzamboni.org/" t nil "Customized with use-package easy-hugo")
 '(gist-view-gist t t nil "Automatically open new gists in browser")
 '(global-visible-mark-mode t)
 '(helm-flx-for-helm-find-files t t nil "Customized with use-package helm-flx")
 '(helm-flx-for-helm-locate t t nil "Customized with use-package helm-flx")
 '(indent-tabs-mode nil)
 '(jiralib-url "https://jira.swisscom.com" nil nil "Customized with use-package org-jira")
 '(js-indent-level 2)
 '(kill-whole-line t)
 '(load-prefer-newer t)
 '(lua-indent-level 2)
 '(mac-command-modifier (quote meta))
 '(mac-option-modifier (quote alt))
 '(mac-right-option-modifier (quote super))
 '(mouse-yank-at-point t)
 '(ns-alternate-modifier (quote alt))
 '(ns-command-modifier (quote meta))
 '(ns-right-alternate-modifier (quote super))
 '(org-agenda-files (quote ("~/tmp/20180522-oce-capability-review.org")))
 '(org-confirm-babel-evaluate nil nil nil "Customized with use-package org")
 '(org-default-notes-file "~/Dropbox/org/notes.org" nil nil "Customized with use-package org")
 '(org-directory "~/Dropbox/org" nil nil "Customized with use-package org")
 '(org-entities-user
   (quote
    (("llangle" "\\llangle" t "&lang;&lang;" "<<" "<<" "《")
     ("rrangle" "\\rrangle" t "&rang;&rang;" ">>" ">>" "》"))))
 '(org-export-with-broken-links t)
 '(org-hide-emphasis-markers t nil nil "Customized with use-package org")
 '(org-hugo-use-code-for-kbd t)
 '(org-journal-dir "~/Documents/logbook" nil nil "Customized with use-package org-journal")
 '(org-latex-compiler "xelatex" nil nil "Customized with use-package ox-latex")
 '(org-latex-pdf-process
   (quote
    ("%latex -shell-escape -interaction nonstopmode -output-directory %o %f" "%latex -interaction nonstopmode -output-directory %o %f" "%latex -interaction nonstopmode -output-directory %o %f")) nil nil "Customized with use-package ox-latex")
 '(org-log-done t nil nil "Customized with use-package org")
 '(org-mac-grab-Acrobat-app-p nil)
 '(org-mac-grab-devonthink-app-p nil)
 '(org-plantuml-jar-path "/usr/local/Cellar/plantuml/1.2018.11/libexec/plantuml.jar" nil nil "Customized with use-package ob-plantuml")
 '(org-reveal-note-key-char nil nil nil "Customized with use-package ox-reveal")
 '(org-reveal-root "file:///Users/taazadi1/Dropbox/org/reveal.js" nil nil "Customized with use-package ox-reveal")
 '(org-src-fontify-natively t nil nil "Customized with use-package org")
 '(org-src-tab-acts-natively t nil nil "Customized with use-package org")
 '(org-startup-indented t nil nil "Customized with use-package org")
 '(org-structure-template-alist
   (quote
    (("a" . "export ascii")
     ("c" . "center")
     ("C" . "comment")
     ("e" . "example")
     ("E" . "export")
     ("h" . "export html")
     ("l" . "export latex")
     ("q" . "quote")
     ("s" . "src")
     ("v" . "verse")
     ("n" . "note")
     ("d" . "description"))))
 '(org-use-speed-commands
   (lambda nil
     (and
      (looking-at org-outline-regexp)
      (looking-back "^**"))) nil nil "Customized with use-package org")
 '(package-archives
   (quote
    (("marmalade" . "https://marmalade-repo.org/packages/")
     ("melpa" . "https://melpa.org/packages/"))))
 '(package-selected-packages
   (quote
    (auth-sources plantuml-mode org-fstree esup package-build org-capture org-babel ox-texinfo gist helm-flx which-key spaceline pretty-mode visual-regexp-steroids ox-hugo adaptive-wrap yankpad smart-mode-line org-plus-contrib ob-cfengine3 org-journal ox-asciidoc org-jira ox-jira org-bullets ox-reveal lispy parinfer uniquify csv all-the-icons toc-org helm cider clojure-mode ido-completing-read+ writeroom-mode crosshairs ox-confluence ox-md inf-ruby ob-plantuml ob-ruby darktooth-theme kaolin-themes htmlize ag col-highlight nix-mode easy-hugo elvish-mode zen-mode racket-mode package-lint scala-mode go-mode wc-mode neotree applescript-mode ack magit clj-refactor yaml-mode visual-fill-column visible-mark use-package unfill typopunct smooth-scrolling smex smartparens rainbow-delimiters projectile markdown-mode magit-popup lua-mode keyfreq imenu-anywhere iedit ido-ubiquitous hl-sexp gruvbox-theme git-commit fish-mode exec-path-from-shell company clojure-mode-extra-font-locking clojure-cheatsheet aggressive-indent adoc-mode 4clojure)))
 '(paradox-automatically-star t nil nil "Customized with use-package paradox")
 '(plantuml-jar-path "/usr/local/Cellar/plantuml/1.2018.11/libexec/plantuml.jar" t nil "Customized with use-package plantuml-mode")
 '(read-buffer-completion-ignore-case t)
 '(read-file-name-completion-ignore-case t)
 '(reb-re-syntax (quote string))
 '(recentf-max-menu-items 100 nil nil "Customized with use-package recentf")
 '(recentf-max-saved-items 100 nil nil "Customized with use-package recentf")
 '(safe-local-variable-values
   (quote
    ((org-hugo-auto-export-on-save . t)
     (org-latex-image-default-width . "0.5\\textwidth")
     (eval progn
           (defun zz/org-macro-hsapi-code
               (link function desc)
             (let*
                 ((link-1
                   (concat link
                           (if
                               (org-string-nw-p function)
                               (concat "#" function)
                             "")))
                  (link-2
                   (concat link
                           (if
                               (org-string-nw-p function)
                               (concat "." function)
                             "")))
                  (desc-1
                   (or
                    (org-string-nw-p desc)
                    (concat "=" link-2 "="))))
               (concat "[[http://www.hammerspoon.org/docs/" link-1 "][" desc-1 "]]")))
           (defun zz/org-macro-keys-code-outer
               (str)
             (mapconcat
              (lambda
                (s)
                (concat "~" s "~"))
              (split-string str)
              (concat
               (string 8203)
               "+"
               (string 8203))))
           (defun zz/org-macro-keys-code-inner
               (str)
             (concat "~"
                     (mapconcat
                      (lambda
                        (s)
                        (concat s))
                      (split-string str)
                      (concat
                       (string 8203)
                       "-"
                       (string 8203)))
                     "~"))
           (defun zz/org-macro-keys-code
               (str)
             (zz/org-macro-keys-code-inner str))
           (defun zz/org-macro-luadoc-code
               (func section desc)
             (let*
                 ((anchor
                   (or
                    (org-string-nw-p section)
                    func))
                  (desc-1
                   (or
                    (org-string-nw-p desc)
                    func)))
               (concat "[[https://www.lua.org/manual/5.3/manual.html#" anchor "][" desc-1 "]]")))
           (defun zz/org-macro-luafun-code
               (func desc)
             (let*
                 ((anchor
                   (concat "pdf-" func))
                  (desc-1
                   (or
                    (org-string-nw-p desc)
                    (concat "=" func "()="))))
               (concat "[[https://www.lua.org/manual/5.3/manual.html#" anchor "][" desc-1 "]]"))))
     (eval add-hook
           (quote after-save-hook)
           (function org-hugo-export-wim-to-md-after-save)
           :append :local)
     (org-adapt-indentation)
     (org-edit-src-content-indentation . 2))))
 '(show-trailing-whitespace t)
 '(sml/replacer-regexp-list
   (quote
    (("^~/\\.emacs\\.d/elpa/" ":ELPA:")
     ("^~/\\.emacs\\.d/" ":ED:")
     ("^/sudo:.*:" ":SU:")
     ("^~/Documents/" ":Doc:")
     ("^:\\([^:]*\\):Documento?s/" ":\\1/Doc:")
     ("^~/Dropbox/" ":DB:")
     ("^:DB:org" ":Org:")
     ("^:DB:Personal/" ":P:")
     ("^:DB:Personal/writing/" ":Write:")
     ("^:P:devel/" ":Dev:")
     ("^:Write:learning-cfengine-3/learning-cfengine-3/" ":cf-learn:")
     ("^:Dev:go/src/github.com/elves/elvish/" ":elvish:")
     ("^:Dev:zzamboni.org/zzamboni.org/" ":zz.org:"))) nil nil "Customized with use-package smart-mode-line")
 '(sml/theme (quote dark) nil nil "Customized with use-package smart-mode-line")
 '(sp-base-key-bindings (quote paredit) nil nil "Customized with use-package smartparens")
 '(tab-width 2)
 '(tool-bar-mode nil)
 '(uniquify-after-kill-buffer-p t nil nil "Customized with use-package uniquify")
 '(uniquify-buffer-name-style (quote post-forward) nil (uniquify) "Customized with use-package uniquify")
 '(uniquify-strip-common-suffix t nil nil "Customized with use-package uniquify")
 '(use-package-always-defer t)
 '(use-package-always-ensure t)
 '(vr/engine (quote pcre2el) nil nil "Use PCRE regular expressions"))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(default ((t (:inherit nil :stipple nil :background "#282828" :foreground "#FDF4C1" :inverse-video nil :box nil :strike-through nil :overline nil :underline nil :slant normal :weight normal :height 160 :width normal :foundry "nil" :family "Inconsolata"))))
 '(col-highlight ((t (:background "#3c3836"))))
 '(fixed-pitch ((t (:family "Inconsolata"))))
 '(font-latex-sedate-face ((t (:inherit fixed-pitch :foreground "#a89984"))))
 '(font-lock-comment-face ((t (:inherit fixed-pitch :foreground "#7c6f64"))))
 '(font-lock-function-name-face ((t (:inherit fixed-pitch :foreground "#fabd2f"))))
 '(linum ((t (:background "#282828" :foreground "#504945" :height 140 :family "Inconsolata"))))
 '(markup-meta-face ((t (:foreground "gray40" :height 140 :family "Inconsolata"))))
 '(markup-title-0-face ((t (:inherit markup-gen-face :height 1.6))))
 '(markup-title-1-face ((t (:inherit markup-gen-face :height 1.5))))
 '(markup-title-2-face ((t (:inherit markup-gen-face :height 1.4))))
 '(markup-title-3-face ((t (:inherit markup-gen-face :weight bold :height 1.3))))
 '(markup-title-5-face ((t (:inherit markup-gen-face :underline t :height 1.1))))
 '(org-block ((t (:inherit fixed-pitch))))
 '(org-code ((t (:inherit (shadow fixed-pitch)))))
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
 '(org-table ((t (:inherit fixed-pitch :foreground "#83a598"))))
 '(org-tag ((t (:inherit (shadow fixed-pitch) :weight bold :height 0.8))))
 '(org-verbatim ((t (:inherit (shadow fixed-pitch)))))
 '(variable-pitch ((t (:weight light :height 180 :family "Source Sans Pro")))))
```


## Password management {#password-management}

Password management using `auth-sources` and `pass` (I normally use 1Password, but I have not found a good command-line/Emacs interface for it, so I am using `pass` for now for some items I need to add to my Emacs config file).

```emacs-lisp
(require 'auth-source)
(require 'auth-source-pass)
(auth-source-pass-enable)
```


## Package management {#package-management}

I use the [wonderful use-package](https://www.masteringemacs.org/article/spotlight-use-package-a-declarative-configuration-tool) to manage most of the packages in my installation (one exception is `org-mode`, see below). As this is not bundled yet with Emacs, the first thing we do is install it by hand. All other packages are then declaratively installed and configured with `use-package`. This makes it possible to fully bootstrap Emacs using only this config file, everything else is downloaded, installed and configured automatically.

First, we declare the package repositories to use.

```emacs-lisp
(customize-set-variable 'package-archives
                        '(;;("gnu"       . "https://elpa.gnu.org/packages/")
                          ("marmalade" . "https://marmalade-repo.org/packages/")
                          ("melpa"     . "https://melpa.org/packages/")))
```

Then we initialize the package system, refresh the list of packages and install `use-package` if needed.

```emacs-lisp
(package-initialize)

(when (not package-archive-contents)
  (package-refresh-contents))

(when (not (package-installed-p 'use-package))
  (package-install 'use-package))
```

Finally, we load `use-package`.

```emacs-lisp
(require 'use-package)
```

We set some configuration for `use-package`:

-   The `use-package-always-ensure` variable indicates that `use-package` should always try to install missing packages. For some libraries this is not appropriate, and in those cases you see the `:ensure nil` declaration as part of the `use-package` statement. This applies mainly to libraries which are installed as part of some other package (happens mostly with some libraries that come with org-mode).

    ```emacs-lisp
    (customize-set-variable 'use-package-always-ensure t)
    ```

-   The `use-package-always-defer` sets `:defer true` as the default for all package declarations. This makes Emacs startup much faster by preventing packages from being loaded when Emacs starts, and only doing so when they are needed. Some packages don't work well with this, so you'll see some declarations when I explicitly set `:defer nil` to force the package to be loaded at startup, or `:defer n` to load the package, but only `n` seconds after startup.

    ```emacs-lisp
    (customize-set-variable 'use-package-always-defer t)
    ```

This variable tells Emacs to prefer the `.el` file if it's newer, even if there is a corresponding `.elc` file. Also, use `auto-compile` to autocompile files as needed.

```emacs-lisp
(customize-set-variable 'load-prefer-newer t)
(use-package auto-compile
  :defer nil
  :config (auto-compile-on-load-mode))
```

Set the load path to the directories from where I sometimes load things outside the package system. Note that the path for `org-mode` (which I load from a checkout of its git repository) is set as part of its `use-package` declaration, so it doesn't appear here.

```emacs-lisp
(add-to-list 'load-path "~/.emacs.d/lisp")
```

Giving a try to [Paradox](https://github.com/Malabarba/paradox) for an enhanced package management interface. We use `auth-sources` to fetch the GitHub token from the `password-store` password manager.

One weirdness: if I set `:defer nil` so that Paradox is loaded right away, the `paradox-github-token` variable gets set with garbage - not sure if this is a bug in `auth-source`, maybe it needs some time to initialize? Setting `:defer 1` (or omitting it, but then Paradox does not get installed as a replacement for `list-packages` until you run `paradox-list-packages` by hand for the first time) results in the correct value being fetched.

(disabled for now)

```emacs-lisp
(use-package paradox
  :defer 1
  :after auth-source-pass
  :config
  (paradox-enable)
  (setq paradox-github-token (auth-source-pass-get 'secret "paradox-github-token"))
  :custom
  (paradox-automatically-star t))
```


## Settings {#settings}


### Proxy settings {#proxy-settings}

These are two short functions I wrote to be able to set/unset proxy settings within Emacs. I haven't bothered to improve or automate this, as I pretty much only need it to be able to install packages sometimes when I'm at work. For now I just call them manually with `M-x zz/(un)set-proxy` when I need to.

```emacs-lisp
(defun zz/set-proxy ()
  (interactive)
  (customize-set-variable 'url-proxy-services '(("http"  . "proxy.corproot.net:8079")
                                                ("https" . "proxy.corproot.net:8079"))))
(defun zz/unset-proxy ()
  (interactive)
  (customize-set-variable 'url-proxy-services nil))
```


### Miscellaneous settings {#miscellaneous-settings}

-   Start the Emacs server

```emacs-lisp
(server-start)
```

-   This is probably one of my oldest settings - I remember adding it around 1993 when I started learning Emacs, and it has been in my config ever since. When `time-stamp` is run before every save, the string `Time-stamp: <>` in the first 8 lines of the file will be updated with the current timestamp.

    ```emacs-lisp
    (add-hook 'before-save-hook 'time-stamp)
    ```

-   When at the beginning of the line, make `Ctrl-K` remove the whole line, instead of just emptying it.

    ```emacs-lisp
    (customize-set-variable 'kill-whole-line t)
    ```

-   Paste text where the cursor is, not where the mouse is.

    ```emacs-lisp
    (customize-set-variable 'mouse-yank-at-point t)
    ```

-   Make completion case-insensitive.

    ```emacs-lisp
    (setq completion-ignore-case t)
    (customize-set-variable 'read-file-name-completion-ignore-case t)
    (customize-set-variable 'read-buffer-completion-ignore-case t)
    ```

-   Show line numbers. I used `linum-mode` before, but it caused severe performance issues on large files. Emacs 26 introduces `display-line-numbers-mode`, which has no perceivable performance impact even on very large files. I still have it disabled by default because I find it a bit distracting.

    ```emacs-lisp
    (when (>= emacs-major-version 26)
      (use-package display-line-numbers
        :disabled
        :defer nil
        :ensure nil
        :config
        (global-display-line-numbers-mode)))
    ```

-   Highlight trailing whitespace in red, so it's easily visible

    ```emacs-lisp
    (customize-set-variable 'show-trailing-whitespace t)
    ```

-   Highlight matching parenthesis

    ```emacs-lisp
    (show-paren-mode)
    ```

-   Don't use hard tabs

    ```emacs-lisp
    (customize-set-variable 'indent-tabs-mode nil)
    ```

-   Emacs automatically creates backup files, by default in the same folder as the original file, which often leaves backup files behind. This tells Emacs to [put all backups in ~/.emacs.d/backups](http://www.gnu.org/software/emacs/manual/html%5Fnode/elisp/Backup-Files.html).

    ```emacs-lisp
    (customize-set-variable 'backup-directory-alist `(("." . ,(concat user-emacs-directory "backups"))))
    ```

-   [WinnerMode](http://emacswiki.org/emacs/WinnerMode) makes it possible to cycle and undo window configuration changes (i.e. arrangement of panels, etc.)

    ```emacs-lisp
    (when (fboundp 'winner-mode) (winner-mode))
    ```

-   Add "unfill" commands to parallel the "fill" ones, bind <kbd>A-q</kbd> to `unfill-paragraph` and rebind <kbd>M-q</kbd> to the `unfill-toggle` command, which fills/unfills paragraphs alternatively.

    ```emacs-lisp
    (use-package unfill
      :bind
      ("M-q" . unfill-toggle)
      ("A-q" . unfill-paragraph))
    ```

-   Save the place of the cursor in each file, and restore it upon opening it again.

    ```emacs-lisp
    (use-package saveplace
      :defer nil
      :config
      (save-place-mode))
    ```

-   Provide mode-specific "bookmarks" - press `M-i` and you will be presented with a list of elements to which you can navigate - they can be headers in org-mode, function names in emacs-lisp, etc.

    ```emacs-lisp
    (use-package imenu-anywhere
      :bind
      ("M-i" . helm-imenu-anywhere))
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

-   Suppress "ad-handle-definition: .. redefined" warnings during Emacs startup.

    ```emacs-lisp
    (customize-set-variable 'ad-redefinition-action 'accept)
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

```emacs-lisp
(customize-set-variable 'mac-command-modifier 'meta)
(customize-set-variable 'mac-option-modifier 'alt)
(customize-set-variable 'mac-right-option-modifier 'super)
```

We also make it possible to use the familiar <kbd>⌘-+</kbd> and <kbd>⌘--</kbd> to increase and decrease the font size. <kbd>⌘-=</kbd> is also bound to "increase" because it's on the same key in an English keyboard.

```emacs-lisp
(bind-key "M-+" 'text-scale-increase)
(bind-key "M-=" 'text-scale-increase)
(bind-key "M--" 'text-scale-decrease)
```

Somewhat surprisingly, there seems to be no "reset" function, so I define my own and bind it to `⌘-0`.

```emacs-lisp
(defun zz/text-scale-reset ()
  (interactive)
  (text-scale-set 0))
(bind-key "M-0" 'zz/text-scale-reset)
```

We also use the `exec-path-from-shell` to make sure the path settings from the shell are loaded into Emacs (usually it starts up with the default system-wide path).

```emacs-lisp
(use-package exec-path-from-shell
  :defer nil
  :config
  (exec-path-from-shell-initialize))
```


### Linux {#linux}

There are no Linux-specific settings for now.


### Windows {#windows}

There are no Windows-specific settings for now.


## Keybindings {#keybindings}

I use the `bind-key` package to more easily keep track and manage user keybindings. `bind-key` comes with `use-package` so we just load it.

The main advantage of using this over `define-key` or `global-set-key` is that you can use <kbd>M-x</kbd> `describe-personal-keybindings` to see a list of all the customized keybindings you have defined.

```emacs-lisp
(require 'bind-key)
```


### Miscellaneous keybindings {#miscellaneous-keybindings}

-   `M-g` interactively asks for a line number and jump to it (`goto-line)`.

    ```emacs-lisp
    (bind-key "M-g" 'goto-line)
    ```

-   `` M-` `` focuses the next frame, if multiple ones are active (emulate the Mac "next app window" keybinding)

    ```emacs-lisp
    (bind-key "M-`" 'other-frame)
    ```

-   Interactive search key bindings -  [visual-regexp-steroids](https://github.com/benma/visual-regexp-steroids.el) provides sane regular expressions and visual incremental search. We make <kbd>C-s</kbd> and <kbd>C-r</kbd> run the visual-regexp functions. We leave <kbd>C-M-s</kbd> and <kbd>C-M-r</kbd> to run the default `isearch-forward/backward` functions, as a fallback. I use the `pcre2el` package to support PCRE-style regular expressions.

    ```emacs-lisp
    (use-package pcre2el)
    (use-package visual-regexp-steroids
      :custom
      (vr/engine 'pcre2el "Use PCRE regular expressions")
      :bind
      ("C-c r" . vr/replace)
      ("C-c q" . vr/query-replace)
      ("C-r"   . vr/isearch-backward)
      ("C-s"   . vr/isearch-forward)
      ("C-M-s" . isearch-forward)
      ("C-M-r" . isearch-backward))
    ```

-   Key binding to use "[hippie expand](http://www.emacswiki.org/emacs/HippieExpand)" for text autocompletion

    ```emacs-lisp
    (bind-key "M-/" 'hippie-expand)
    ```

-   The [which-key](https://github.com/justbur/emacs-which-key) package makes Emacs functionality much easier to discover and explore: in short, after you start the input of a command and stop, pondering what key must follow, it will automatically open a non-intrusive buffer at the bottom of the screen offering you suggestions for completing the command, that's it, nothing else. It's beautiful.

    ```emacs-lisp
    (use-package which-key
      :defer nil
      :diminish which-key-mode
      :config
      (which-key-mode))
    ```


### Emulating vi's `%` key {#emulating-vi-s-key}

One of the few things I missed in Emacs from vi was the `%` key, which jumps to the parenthesis, bracket or brace which matches the one below the cursor. This function implements the functionality. Inspired by <http://www.emacswiki.org/emacs/NavigatingParentheses>, but modified to use `smartparens` instead of the default commands, and to work on brackets and braces.

```emacs-lisp
(defun zz/goto-match-paren (arg)
  "Go to the matching paren/bracket, otherwise (or if ARG is not nil) insert %.
  vi style of % jumping to matching brace."
  (interactive "p")
  (if (not (memq last-command '(set-mark
                                cua-set-mark
                                zz/goto-match-paren
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
                                back-to-indentation
                                )))
      (self-insert-command (or arg 1))
    (cond ((looking-at "\\s\(") (sp-forward-sexp) (backward-char 1))
          ((looking-at "\\s\)") (forward-char 1) (sp-backward-sexp))
          (t (self-insert-command (or arg 1))))))
```

We bind this function to the `%` key.

```emacs-lisp
(bind-key "%" 'zz/goto-match-paren)
```


## Org mode {#org-mode}

I have started using [org-mode](http://orgmode.org/) to writing, blogging, coding, presentations and more, thanks to the hearty recommendations and information from [Nick](http://www.cmdln.org/) and many others. I am duly impressed. I have been a fan of the idea of [literate programming](https://en.wikipedia.org/wiki/Literate%5Fprogramming) for many years, and I have tried other tools before (most notably [noweb](https://www.cs.tufts.edu/~nr/noweb/), which I used during grad school for many of my homeworks and projects), but org-mode is the first tool I have encountered which seems to make it practical. Here are some of the resources I have found useful in learning it:

-   Howard Abrams' [Introduction to Literate Programming](http://www.howardism.org/Technical/Emacs/literate-programming-tutorial.html), which got me jumpstarted into writing code documented with org-mode.
-   Nick Anderson's [Level up your notes with Org](https://github.com/nickanderson/Level-up-your-notes-with-Org), which contains many useful tips and configuration tricks.
-   Sacha Chua's [Some tips for learning Org Mode for Emacs](http://sachachua.com/blog/2014/01/tips-learning-org-mode-emacs/), her [Emacs configuration](http://pages.sachachua.com/.emacs.d/Sacha.html) and many of her [other articles](http://sachachua.com/blog/category/emacs/).
-   Rainer König's [OrgMode Tutorial](https://www.youtube.com/playlist?list=PLVtKhBrRV%5FZkPnBtt%5FTD1Cs9PJlU0IIdE) video series.

This is the newest and most-in-flux section of my Emacs config, since I'm still learning org-mode myself.

I use `use-package` to load the `org` package, and put its configuration inside the corresponding sections for keybindings (`:bind`), custom variables (`:custom`), custom faces (`:custom-face`), hooks (`:hook`) and general configuration code (`:config`), respectively. The contents of each section is populated with the corresponding snippets that follow. You see here the complete `use-package` declaration for completeness, but see the sections below for the details on where each snippet comes from, and some other configuration code that ends up outside this declaration.

```emacs-lisp
(use-package org
  :pin manual
  :load-path ("lisp/org-mode/lisp" "lisp/org-mode/lisp/contrib/lisp")
  :bind
    ("C-c l" . org-store-link)
    ("C-c a" . org-agenda)
    ("A-h" . org-mark-element)
    ("C-c c" . org-capture)
  :custom
    (org-log-done t)
    (org-startup-indented t)
    (org-use-speed-commands (lambda () (and (looking-at org-outline-regexp) (looking-back "^\**"))))
    (org-confirm-babel-evaluate nil)
    (org-src-fontify-natively t)
    (org-src-tab-acts-natively t)
    (org-hide-emphasis-markers t)
  :custom-face
    (variable-pitch ((t (:family "Source Sans Pro" :height 160 :weight light))))
    ;;(variable-pitch ((t (:family "Avenir Next" :height 160 :weight light))))
    (fixed-pitch ((t (:family "Inconsolata"))))
  :hook
    (org-babel-after-execute . org-redisplay-inline-images)
    (org-mode . (lambda () (add-hook 'after-save-hook 'org-babel-tangle
                                     'run-at-end 'only-in-org-mode)))
    (org-babel-pre-tangle  . (lambda ()
                               (setq zz/pre-tangle-time (current-time))))
    (org-babel-post-tangle . (lambda ()
                               (message "org-babel-tangle took %s"
                                               (format "%.2f seconds"
                                                       (float-time (time-since zz/pre-tangle-time))))))
    (org-mode . visual-line-mode)
    (org-mode . variable-pitch-mode)
  :config
    (org-babel-do-load-languages
     'org-babel-load-languages
     '((cfengine3 . t)
       (ruby      . t)
       (latex     . t)
       (plantuml  . t)
       (python    . t)
       (shell     . t)
       (elvish    . t)
       (calc      . t)))
    (font-lock-add-keywords 'org-mode
                            '(("^ *\\([-]\\) "
                               (0 (prog1 () (compose-region (match-beginning 1) (match-end 1) "•"))))))
    (let* ((variable-tuple
            (cond ((x-list-fonts   "Source Sans Pro") '(:font   "Source Sans Pro"))
                  ((x-list-fonts   "Lucida Grande")   '(:font   "Lucida Grande"))
                  ((x-list-fonts   "Verdana")         '(:font   "Verdana"))
                  ((x-family-fonts "Sans Serif")      '(:family "Sans Serif"))
                  (nil (warn "Cannot find a Sans Serif Font.  Install Source Sans Pro."))))
           (base-font-color (face-foreground 'default nil 'default))
           (headline       `(:inherit default :weight bold :foreground ,base-font-color)))

      (custom-theme-set-faces
       'user
       `(org-level-8        ((t (,@headline ,@variable-tuple))))
       `(org-level-7        ((t (,@headline ,@variable-tuple))))
       `(org-level-6        ((t (,@headline ,@variable-tuple))))
       `(org-level-5        ((t (,@headline ,@variable-tuple))))
       `(org-level-4        ((t (,@headline ,@variable-tuple :height 1.1))))
       `(org-level-3        ((t (,@headline ,@variable-tuple :height 1.25))))
       `(org-level-2        ((t (,@headline ,@variable-tuple :height 1.5))))
       `(org-level-1        ((t (,@headline ,@variable-tuple :height 1.75))))
       `(org-document-title ((t (,@headline ,@variable-tuple :height 2.0 :underline nil))))))
    (eval-after-load 'face-remap '(diminish 'buffer-face-mode))
    (eval-after-load 'simple '(diminish 'visual-line-mode)))
```


### General org-mode configuration {#general-org-mode-configuration}

Automatically log done times in todo items.

```emacs-lisp
(org-log-done t)
```

Keep the indentation well structured by setting `org-startup-indented` to `t`. This is a must have. Makes it feel less like editing a big text file and more like a purpose built editor for org-mode that forces the indentation. Thanks [Nick](https://github.com/nickanderson/Level-up-your-notes-with-Org/blob/master/Level-up-your-notes-with-Org.org#automatic-visual-indention) for the tip!

```emacs-lisp
(org-startup-indented t)
```

By default, `org-indent` produces an indicator `"Ind"` in the modeline. We use diminish to hide it.

```emacs-lisp
(use-package org-indent
  :ensure nil
  :diminish)
```


### Miscellaneous org functions {#miscellaneous-org-functions}

Utility `org-get-keyword` function (from the org-mode mailing list) to get the value of file-level properties.

```emacs-lisp
(defun org-get-keyword (key)
  (org-element-map (org-element-parse-buffer 'element) 'keyword
    (lambda (k)
      (when (string= key (org-element-property :key k))
        (org-element-property :value k)))
    nil t))
```


### Keybindings {#keybindings}

Set up `C-c l` to store a link to the current org object, in counterpart to the default `C-c C-l` to insert a link.

```emacs-lisp
("C-c l" . org-store-link)
```

Set up `C-c a` to call up agenda mode.

```emacs-lisp
("C-c a" . org-agenda)
```

The default keybinding for `org-mark-element` is `M-h`, which in macOS hides the current application, so I bind it to `A-h`.

```emacs-lisp
("A-h" . org-mark-element)
```

Default setup and keybinding for `org-capture`.

```emacs-lisp
("C-c c" . org-capture)
```

Load `org-tempo` to enable snippets such as `<s<TAB>` to insert a source block. Disabled for now as I try to get used to the new <kbd>C-c</kbd> <kbd>C-,</kbd> shortcut recently introduced. See the loooong discussion starting at <https://lists.gnu.org/archive/html/emacs-orgmode/2018-04/msg00600.html>.

```emacs-lisp
(use-package org-tempo
  :disabled
  :defer 5
  :ensure nil
  :after org)
```

Enable [Speed Keys](https://orgmode.org/manual/Speed-keys.html), which allows quick single-key commands when the cursor is placed on a heading. Usually the cursor needs to be at the beginning of a headline line, but defining it with this function makes them active on any of the asterisks at the beginning of the line (useful with the font highlighting I use, as all but the last asterisk are sometimes not visible).

```emacs-lisp
(org-use-speed-commands (lambda () (and (looking-at org-outline-regexp) (looking-back "^\**"))))
```


### Building presentations with org-mode {#building-presentations-with-org-mode}

[org-reveal](https://github.com/yjwen/org-reveal) is an awesome package for building presentations with org-mode. The MELPA version of the package gives me a conflict with my hand-installed version of org-mode, so I also install it by hand and load it directly from its checked-out repository.

```emacs-lisp
(use-package ox-reveal
  :load-path ("lisp/org-reveal")
  :defer 3
  :after org
  :custom
  (org-reveal-note-key-char nil)
  (org-reveal-root "file:///Users/taazadi1/Dropbox/org/reveal.js"))
(use-package htmlize
  :defer 3
  :after ox-reveal)
```


### Various exporters {#various-exporters}

One of the big strengths of org-mode is the ability to export a document in many different formats. Here I load some of the exporters I have found useful.

-   Markdown

    ```emacs-lisp
    (use-package ox-md
      :ensure nil
      :defer 3
      :after org)
    ```

-   [Jira markup](https://github.com/stig/ox-jira.el). I also load `org-jira`, which provides a full interface to Jira through org-mode.

    ```emacs-lisp
    (use-package ox-jira
      :defer 3
      :after org)
    (use-package org-jira
      :defer 3
      :after org
      :custom
      (jiralib-url "https://jira.swisscom.com"))
    ```

-   Confluence markup.

    ```emacs-lisp
    (use-package ox-confluence
      :defer 3
      :ensure nil
      :after org)
    ```

-   AsciiDoc

    ```emacs-lisp
    (use-package ox-asciidoc
      :defer 3
      :after org)
    ```

-   TexInfo. I have found that the best way to produce a PDF from an org file is to export it to a `.texi` file, and then use `texi2pdf` to produce the PDF.

    ```emacs-lisp
    (use-package ox-texinfo
      :load-path "lisp/org-mode/lisp"
      :defer 3
      :ensure nil
      :after org)
    ```

-   Some customizations for the LaTeX exporter. `ox-latex` gets loaded automatically, but we use `use-package` anyway so that the config code is only executed after the package is loaded. I add a pseudo-class which uses the document class `book` but without parts (only chapters at the top level).

    ```emacs-lisp
    (use-package ox-latex
      :load-path "lisp/org-mode/lisp"
      :ensure nil
      :demand
      :after org
      :custom
      (org-latex-compiler "xelatex")
      (org-latex-pdf-process '("%latex -shell-escape -interaction nonstopmode -output-directory %o %f" "%latex -interaction nonstopmode -output-directory %o %f" "%latex -interaction nonstopmode -output-directory %o %f"))
      :config
      (setq org-latex-listings 'minted)
      (add-to-list 'org-latex-packages-alist '("newfloat" "minted"))
      (add-to-list 'org-latex-minted-langs '(lua "lua"))
      (add-to-list 'org-latex-minted-langs '(shell "shell"))
      (add-to-list 'org-latex-classes '("book-no-parts" "\\documentclass[11pt,letterpaper]{book}"
                                        ("\\chapter{%s}" . "\\chapter*{%s}")
                                        ("\\section{%s}" . "\\section*{%s}")
                                        ("\\subsection{%s}" . "\\subsection*{%s}")
                                        ("\\subsubsection{%s}" . "\\subsubsection*{%s}")
                                        ("\\paragraph{%s}" . "\\paragraph*{%s}")))
      (add-to-list 'org-latex-classes '("awesome-cv" "\\documentclass{awesome-cv}"
                                        ("\\cvsection{%s}" . "\\cvsection{%s}")
                                        ("\\cvsubsection{%s}" . "\\cvsubsection{%s}")
                                        ("\\subsection{%s}" . "\\subsection*{%s}")
                                        ("\\subsubsection{%s}" . "\\subsubsection*{%s}")
                                        ("\\cvparagraph{%s}" . "\\cvparagraph{%s}")))
      ;; Necessary for LuaLaTeX to work - see https://tex.stackexchange.com/a/374391/10680
      (setenv "LANG" "en_US.UTF-8"))
    ```


### Blogging with Hugo {#blogging-with-hugo}

[ox-hugo](https://ox-hugo.scripter.co/) is an awesome way to blog from org-mode. It makes it possible for posts in org-mode format to be kept separate, and it generates the Markdown files for Hugo. Hugo [supports org files](https://gohugo.io/content-management/formats/), but using ox-hugo has multiple advantages:

-   Parsing is done by org-mode natively, not by an external library. Although goorgeous (used by Hugo) is very good, it still lacks in many areas, which leads to text being interpreted differently as by org-mode.
-   Hugo is left to parse a native Markdown file, which means that many of its features such as shortcodes, TOC generation, etc., can still be used on the generated file.
-   I am intrigued by ox-hugo's "one post per org subtree" proposed structure. So far I've always had one file per post, but with org-mode's structuring features, it might make sense to give it a try.

We load `ox-hugo` followed by `ox-hugo-auto-export`, to set up [Auto-export on saving](https://ox-hugo.scripter.co/doc/auto-export-on-saving/).

```emacs-lisp
(use-package ox-hugo
  :defer 3
  :after org
  :config
  (require 'ox-hugo-auto-export))
```

Configure a capture template for creating new ox-hugo blog posts, from [ox-hugo's Org Capture Setup](https://ox-hugo.scripter.co/doc/org-capture-setup).

```emacs-lisp
(use-package org-capture
  :ensure nil
  :config
  (defun org-hugo-new-subtree-post-capture-template ()
    "Returns `org-capture' template string for new Hugo post.
  See `org-capture-templates' for more information."
    (let* ((title (read-from-minibuffer "Post Title: ")) ;Prompt to enter the post title
           (fname (org-hugo-slug title)))
      (mapconcat #'identity
                 `(,(concat "* TODO " title)
                   ":PROPERTIES:"
                   ,(concat ":EXPORT_HUGO_BUNDLE: " fname)
                   ":EXPORT_FILE_NAME: index"
                   ":END:"
                   "%?\n")                ;Place the cursor here finally
                 "\n")))
  (add-to-list 'org-capture-templates
               '("z"                ;`org-capture' binding + z
                 "zzamboni.org post"
                 entry
                 ;; It is assumed that below file is present in `org-directory'
                 ;; and that it has an "Ideas" heading. It can even be a
                 ;; symlink pointing to the actual location of all-posts.org!
                 (file+olp "zzamboni.org" "Ideas")
                 (function org-hugo-new-subtree-post-capture-template))))
```


### Keeping a Journal {#keeping-a-journal}

I use [750words](http://750words.com/) for my personal Journal, and I usually write my entries locally using Scrivener. I have been playing with `org-journal` for this, but I am not fully convinced yet.

```emacs-lisp
(use-package org-journal
  :after org
  :custom
  (org-journal-dir "~/Documents/logbook"))
```


### Literate programming using org-babel {#literate-programming-using-org-babel}

Org-mode is the first literate programming tool that seems practical and useful, since it's easy to edit, execute and document code from within the same tool (Emacs) using all of its existing capabilities (i.e. each code block can be edited in its native Emacs mode, taking full advantage of indentation, completion, etc.)

Plain literate programming is built-in, but the `ob-*` packages provide the ability to execute code in different languages, beyond those included with org-mode.

```emacs-lisp
(use-package ob-cfengine3
  :after org)
```

```emacs-lisp
(use-package ob-elvish
  :after org)
```

For [PlantUML](http://plantuml.com/) graph language, we install first the general `plantuml-mode` and the associated `org-babel` mode. We determine the location of the PlantUML jar file automatically from the installed Homebrew formula, and use it to configure both `ob-plantuml` and `plantuml-mode`.

```emacs-lisp
(require 'subr-x)
(setq homebrew-plantuml-jar-path
      (expand-file-name (string-trim (shell-command-to-string "brew list plantuml | grep jar"))))

(use-package plantuml-mode
  :custom
  (plantuml-jar-path homebrew-plantuml-jar-path))

(use-package ob-plantuml
  :ensure nil
  :after org
  :custom
  (org-plantuml-jar-path homebrew-plantuml-jar-path))
```

Define `shell-script-mode` as an alias for `console-mode`, so that `console` src blocks can be edited and are fontified correctly.

```emacs-lisp
(defalias 'console-mode 'shell-script-mode)
```

We configure the languages for which to load org-babel support.

```emacs-lisp
(org-babel-do-load-languages
 'org-babel-load-languages
 '((cfengine3 . t)
   (ruby      . t)
   (latex     . t)
   (plantuml  . t)
   (python    . t)
   (shell     . t)
   (elvish    . t)
   (calc      . t)))
```

This is potentially dangerous: it suppresses the query before executing code from within org-mode. I use it because I am very careful and only press `C-c C-c` on blocks I absolutely understand.

```emacs-lisp
(org-confirm-babel-evaluate nil)
```

This makes it so that code within `src` blocks is fontified according to their corresponding Emacs mode, making the file much more readable.

```emacs-lisp
(org-src-fontify-natively t)
```

In principle this makes it so that indentation in `src` blocks works as in their native mode, but in my experience it does not always work reliably. For full proper indentation, always edit the code in a native buffer by pressing `C-c '`.

```emacs-lisp
(org-src-tab-acts-natively t)
```

Automatically show inline images, useful when executing code that produces them, such as PlantUML or Graphviz.

```emacs-lisp
(org-babel-after-execute . org-redisplay-inline-images)
```

This little snippet has revolutionized my literate programming workflow. It automatically runs `org-babel-tangle` upon saving any org-mode buffer, which means the resulting files will be automatically kept up to date.

```emacs-lisp
(org-mode . (lambda () (add-hook 'after-save-hook 'org-babel-tangle
                                 'run-at-end 'only-in-org-mode)))
```

I add hooks to measure and report how long the tangling took.

```emacs-lisp
(org-babel-pre-tangle  . (lambda ()
                           (setq zz/pre-tangle-time (current-time))))
(org-babel-post-tangle . (lambda ()
                           (message "org-babel-tangle took %s"
                                           (format "%.2f seconds"
                                                   (float-time (time-since zz/pre-tangle-time))))))
```


### Beautifying org-mode {#beautifying-org-mode}

These settings make org-mode much more readable by using different fonts for headings, hiding some of the markup, etc. This was taken originally from Howard Abrams' [Org as a Word Processor](http://www.howardism.org/Technical/Emacs/orgmode-wordprocessor.html), and subsequently tweaked and broken up in the different parts of the `use-package` declaration by me.

First, we set `org-hid-emphasis-markers` so that the markup indicators are not shown.

```emacs-lisp
(org-hide-emphasis-markers t)
```

We add an entry to the org-mode font-lock table so that list markers are shown with a middle dot instead of the original character.

```emacs-lisp
(font-lock-add-keywords 'org-mode
                        '(("^ *\\([-]\\) "
                           (0 (prog1 () (compose-region (match-beginning 1) (match-end 1) "•"))))))
```

We use the `org-bullets` package to display the titles with nice unicode bullets instead of the text ones.

```emacs-lisp
(use-package org-bullets
  :after org
  :hook
  (org-mode . (lambda () (org-bullets-mode 1))))
```

We choose a nice font for the document title and the section headings. The first one found in the system from the list below is used, and the same font is used for the different levels, in varying sizes.

```emacs-lisp
(let* ((variable-tuple
        (cond ((x-list-fonts   "Source Sans Pro") '(:font   "Source Sans Pro"))
              ((x-list-fonts   "Lucida Grande")   '(:font   "Lucida Grande"))
              ((x-list-fonts   "Verdana")         '(:font   "Verdana"))
              ((x-family-fonts "Sans Serif")      '(:family "Sans Serif"))
              (nil (warn "Cannot find a Sans Serif Font.  Install Source Sans Pro."))))
       (base-font-color (face-foreground 'default nil 'default))
       (headline       `(:inherit default :weight bold :foreground ,base-font-color)))

  (custom-theme-set-faces
   'user
   `(org-level-8        ((t (,@headline ,@variable-tuple))))
   `(org-level-7        ((t (,@headline ,@variable-tuple))))
   `(org-level-6        ((t (,@headline ,@variable-tuple))))
   `(org-level-5        ((t (,@headline ,@variable-tuple))))
   `(org-level-4        ((t (,@headline ,@variable-tuple :height 1.1))))
   `(org-level-3        ((t (,@headline ,@variable-tuple :height 1.25))))
   `(org-level-2        ((t (,@headline ,@variable-tuple :height 1.5))))
   `(org-level-1        ((t (,@headline ,@variable-tuple :height 1.75))))
   `(org-document-title ((t (,@headline ,@variable-tuple :height 2.0 :underline nil))))))
```

I use proportional fonts in org-mode for the text, while keeping fixed-width fonts for blocks, so that source code, tables, etc. are shown correctly. These settings include:

-   Setting up the `variable-pitch` face to the proportional font I like to use. I'm currently alternating between my two favorites, [Source Sans Pro](https://en.wikipedia.org/wiki/Source%5FSans%5FPro) and [Avenir Next](https://en.wikipedia.org/wiki/Avenir%5F(typeface)).

    ```emacs-lisp
    (variable-pitch ((t (:family "Source Sans Pro" :height 160 :weight light))))
    ;;(variable-pitch ((t (:family "Avenir Next" :height 160 :weight light))))
    ```

-   Setting up the `fixed-pitch` face to be the same as my usual `default` face. My current one is [Inconsolata](https://en.wikipedia.org/wiki/Inconsolata).

    ```emacs-lisp
    (fixed-pitch ((t (:family "Inconsolata"))))
    ```

-   Configuring the corresponding `org-mode` faces for blocks, verbatim code, and maybe a couple of other things. As these change more frequently, I do them directly from the `customize-face` interface, you can see their current settings in the [Customized variables](#customized-variables) section.

-   Setting up `visual-line-mode` and making all my paragraphs one single line, so that the lines wrap around nicely in the window according to their proportional-font size, instead of at a fixed character count, which does not work so nicely when characters have varying widths. I set up a hook that automatically enables `visual-line-mode` and `variable-pitch-mode` when entering org-mode.

    ```emacs-lisp
    (org-mode . visual-line-mode)
    (org-mode . variable-pitch-mode)
    ```

    These two modes produce modeline indicators, which I disable using `diminish`.

    ```emacs-lisp
    (eval-after-load 'face-remap '(diminish 'buffer-face-mode))
    (eval-after-load 'simple '(diminish 'visual-line-mode))
    ```


### Auto-generated table of contents {#auto-generated-table-of-contents}

The `toc-org` package allows us to insert a table of contents in headings marked with `:TOC:`. This is useful for org files that are to be viewed directly on GitHub, which renders org files correctly, but does not generate a table of contents at the top. For an example, see [this file on GitHub](https://github.com/zzamboni/dot-emacs/blob/master/init.org).

Note that this breaks HTML export by default, as the links generated by `toc-org` cannot be parsed properly by the html exporter. The [workaround](https://github.com/snosov1/toc-org/issues/35#issuecomment-275096511) is to use `:TOC:noexport:` as the marker, which removed the generated TOC from the export, but still allows `ox-html` to insert its own TOC at the top.

```emacs-lisp
(use-package toc-org
  :after org
  :hook
  (org-mode . toc-org-enable))
```


### Grabbing links from different Mac applications {#grabbing-links-from-different-mac-applications}

`org-mac-link` (included in contrib) implements the ability to grab links from different Mac apps and insert them in the file. Bind `C-c g` to call `org-mac-grab-link` to choose an application and insert a link.

```emacs-lisp
(use-package org-mac-link
  :ensure nil
  :load-path "lisp/org-mode/contrib/lisp"
  :after org
  :bind (:map org-mode-map
              ("C-c g" . org-mac-grab-link)))
```


### Reformatting an org buffer {#reformatting-an-org-buffer}

I picked up this little gem in the org mailing list. A function that reformats the current buffer by regenerating the text from its internal parsed representation. Quite amazing.

```emacs-lisp
(defun zz/org-reformat-buffer ()
  (interactive)
  (when (y-or-n-p "Really format current buffer? ")
    (let ((document (org-element-interpret-data (org-element-parse-buffer))))
      (erase-buffer)
      (insert document)
      (goto-char (point-min)))))
```

Remove a link. For some reason this is not part of org-mode. From <https://emacs.stackexchange.com/a/10714/11843>, I bind it to <kbd>C-c</kbd> <kbd>C-M-u</kbd>.

```emacs-lisp
(defun afs/org-replace-link-by-link-description ()
    "Replace an org link by its description or if empty its address"
  (interactive)
  (if (org-in-regexp org-bracket-link-regexp 1)
      (let ((remove (list (match-beginning 0) (match-end 0)))
        (description (if (match-end 3)
                 (org-match-string-no-properties 3)
                 (org-match-string-no-properties 1))))
    (apply 'delete-region remove)
    (insert description))))
(bind-key "C-c C-M-u" 'afs/org-replace-link-by-link-description)
```


### Code for org-mode macros {#code-for-org-mode-macros}

Here I define functions which get used in some of my org-mode macros

This function receives three arguments, and returns the org-mode code for a link to the Hammerspoon API documentation for the `link` module, optionally to a specific `function`. If `desc` is passed, it is used as the display text, otherwise `section.function` is used.

```emacs-lisp
(defun zz/org-macro-hsapi-code (link function desc)
  (let* ((link-1 (concat link (if (org-string-nw-p function) (concat "#" function) "")))
         (link-2 (concat link (if (org-string-nw-p function) (concat "." function) "")))
         (desc-1 (or (org-string-nw-p desc) (concat "=" link-2 "="))))
    (concat "[[http://www.hammerspoon.org/docs/" link-1 "][" desc-1 "]]")))
```

Split STR at spaces and wrap each element with `~` char, separated by `+`. Zero-width spaces are inserted around the plus signs so that they get formatted correctly.

```emacs-lisp
(defun zz/org-macro-keys-code-outer (str)
  (mapconcat (lambda (s)
               (concat "~" s "~"))
             (split-string str)
             (concat (string ?\u200B) "+" (string ?\u200B))))
(defun zz/org-macro-keys-code-inner (str)
  (concat "~" (mapconcat (lambda (s)
                           (concat s))
                         (split-string str)
                         (concat (string ?\u200B) "-" (string ?\u200B)))
          "~"))
(defun zz/org-macro-keys-code (str)
  (zz/org-macro-keys-code-inner str))
```

Links to a specific section/function of the Lua manual.

```emacs-lisp
(defun zz/org-macro-luadoc-code (func section desc)
  (let* ((anchor (or (org-string-nw-p section) func))
         (desc-1 (or (org-string-nw-p desc) func)))
    (concat "[[https://www.lua.org/manual/5.3/manual.html#" anchor "][" desc-1 "]]")))
```

```emacs-lisp
(defun zz/org-macro-luafun-code (func desc)
  (let* ((anchor (concat "pdf-" func))
         (desc-1 (or (org-string-nw-p desc) (concat "=" func "()="))))
    (concat "[[https://www.lua.org/manual/5.3/manual.html#" anchor "][" desc-1 "]]")))
```


### Publishing project configuration {#publishing-project-configuration}

Define a publishing function based on `org-latex-publish-to-pdf` but which opens the resulting file at the end.

```emacs-lisp
(defun org-latex-publish-to-latex-and-open (plist file pub-dir)
  (org-open-file (org-latex-publish-to-pdf plist file pub-dir)))
```

Sample project configuration - disabled for now because this configuration has been incorporated into the `structure.tex` file and in the general `ox-latex` configuration, but kept here as a sample.

```emacs-lisp
(org-publish-project-alist
 '(("mac-automation"
    :base-directory "~/Personal/writing/mac-automation/"
    :publishing-directory "~/Personal/writing/mac-automation/build/"
    :base-extension "org"
    :publishing-function org-latex-publish-to-latex-and-open
    :latex-compiler "xelatex"
    :latex-classes '("book-no-parts" "\\documentclass[11pt]{book}"
                      ("\\chapter{%s}" . "\\chapter*{%s}")
                      ("\\section{%s}" . "\\section*{%s}")
                      ("\\subsection{%s}" . "\\subsection*{%s}")
                      ("\\subsubsection{%s}" . "\\subsubsection*{%s}")
                      ("\\paragraph{%s}" . "\\paragraph*{%s}"))
    :latex-class "book-no-parts"
    :latex-title-command "\\makeatletter\\begingroup
  \\thispagestyle{empty}
  \\begin{tikzpicture}[remember picture,overlay]
  \\node[inner sep=0pt] (background) at (current page.center) {\\includegraphics[width=\\paperwidth]{background}};
  \\draw (current page.center) node [fill=ocre!30!white,fill opacity=0.6,text opacity=1,inner sep=1cm]{\\Huge\\centering\\bfseries\\sffamily\\parbox[c][][t]{\\paperwidth}{\\centering \\@title \\\\[15pt]
  {\\Large \\@subtitle }\\\\[20pt]
  {\\huge \\@author }}};
  \\end{tikzpicture}
  \\vfill
  \\endgroup\\makeatother
  \\chapterimage{chapter_head_1.pdf}"
    :latex-toc-command "\\pagestyle{empty}
\\tableofcontents
\\cleardoublepage
\\pagestyle{fancy}"
    )))
```


### Publishing to LeanPub {#publishing-to-leanpub}

I use [LeanPub](https://leanpub.com/) for self-publishing my books [Learning Hammerspoon](https://leanpub.com/learning-hammerspoon/) and [Learning CFEngine](https://leanpub.com/learning-cfengine/). Fortunately, it is possible to export from org-mode to LeanPub-flavored Markdown.

Some references:

-   [Description of ox-leanpub.el](http://juanreyero.com/open/ox-leanpub/index.html) ([GitHub repo](https://github.com/juanre/ox-leanpub)) by [Juan Reyero](http://juanreyero.com/about/)
-   [Publishing a book using org-mode](https://medium.com/@lakshminp/publishing-a-book-using-org-mode-9e817a56d144) by [Lakshmi Narasimhan](https://medium.com/@lakshminp/publishing-a-book-using-org-mode-9e817a56d144)
-   [Writing a book with emacs org-mode and Leanpub](https://web.archive.org/web/20170816044305/http://anbasile.github.io/writing/2017/04/08/orgleanpub.html) by Angelo Basile (the link goes to an archive copy of the post, as it is not live on his website anymore)
-   [Publishing a Book with Leanpub and Org Mode](http://irreal.org/blog/?p=5313) by Jon Snader (from where I found the links to the above)

First, load `ox-leanpub`. As part of its configuration, I define a new export backend called `leanpub-multifile`, which adds three additional items in the LeanPub export section:

-   "Multifile Export", which calls `leanpub-export` (defined below) with its default settings, to export the whole book as one-file-per-chapter;
-   "Multifile Export (subset)", which calls `leanpub-export` with the `subset-only` flag set, which means only the `Subset.txt` file is exported. I use this together with `#+LEANPUB_WRITE_SUBSET: current` in my files to quickly export only the current chapter, to be able to quickly preview it using [LeanPub's subset-preview feature](https://leanpub.com/help/manual#subsetpreview);
-   "Export current chapter" to explicitly export only the current chapter to its own file. This also updates `Subset.txt`, so it can be used to preview the current chapter without having to set `#+LEANPUB_WRITE_SUBSET: current`.

```emacs-lisp
(use-package ox-leanpub
  :ensure nil
  :defer 3
  :after org
  :load-path ("lisp/ox-leanpub")
  :config (org-export-define-derived-backend 'leanpub-multifile 'leanpub
            :menu-entry
            '(?L 1
                 ((?p "Multifile Export" (lambda (a s v b) (leanpub-export a s v b)))
                  (?s "Multifile Export (subset)" (lambda (a s v b) (leanpub-export a s v b t)))
                  (?c "Export current chapter" (lambda (a s v b) (leanpub-export a s v b t "current")))))
            :options-alist
            '((:leanpub-output-dir "LEANPUB_OUTPUT_DIR" nil "manuscript" t)
              (:leanpub-write-subset "LEANPUB_WRITE_SUBSET" nil nil t))
            ))
```

Next, the `leanpub-export` function, which does the work of splitting chapters into files, and to automatically populate the `Book.txt`, `Sample.txt` and `Subset.txt` files used by LeanPub. Based on the code from [Lakshmi's post](https://medium.com/@lakshminp/publishing-a-book-using-org-mode-9e817a56d144), but with the following additions:

-   The exported files are written to the `manuscript/` subdirectory by default, which is what LeanPub expects. This default allows me to keep my book's main `org` file in the top-level directory of my repository, and to automatically write the output files to `manuscript/` so that LeanPub can process them. However, the output directory can be changed using the `#+LEANPUB_OUTPUT_DIR` file property, for example if you want to export to the current directory, you can use:

    ```text
    #+LEANPUB_OUTPUT_DIR: .
    ```
-   The book files are populated as follows:
    -   `Book.txt` with all chapters, except those tagged with `noexport`.
    -   `Sample.txt` with all chapters tagged with `sample`.
    -   `Subset.txt` with chapters depending on the value of the `#+LEANPUB_WRITE_SUBSET` file property (if set):
        -   Default: not created.
        -   `tagged`: use all chapters tagged `subset`.
        -   `all`: use the same chapters as `Book.txt`.
        -   `sample`: use same chapters as `Sample.txt`.
        -   `current`: export the current chapter (where the cursor is at the moment of the export) as the contents of `Subset.txt`.
-   If a heading has the `frontmatter`, `mainmatter` or `backmatter` tags, the corresponding markup is inserted in the output, before the headline. This way, you only need to tag the first chapter of the front, main, and backmatter, respectively.
-   Each section's headline is exported as part of the output (it is not in the original code)

```emacs-lisp
(defun leanpub-export (&optional async subtreep visible-only body-only only-subset subset-type)
  "Export buffer to a Leanpub book."
  (interactive)
  (let* ((info (org-combine-plists
                (org-export--get-export-attributes
                 'leanpub-multifile subtreep visible-only)
                (org-export--get-buffer-attributes)
                (org-export-get-environment 'leanpub-multifile subtreep)))
         (outdir (plist-get info :leanpub-output-dir))
         (do-subset (or subset-type (plist-get info :leanpub-write-subset)))
         (matter-tags '("frontmatter" "mainmatter" "backmatter"))
         (original-point (point)))
    ;; Relative pathname given the basename of a file, including the correct output dir
    (fset 'outfile (lambda (f) (concat outdir "/" f)))
    ;; delete all these files, they get recreated as needed
    (dolist (fname (mapcar (lambda (s) (concat s ".txt"))
                           (append (if only-subset '("Subset") '("Book" "Sample" "Subset"))
                                   matter-tags)))
      (delete-file (outfile fname)))
    (save-mark-and-excursion
      (org-map-entries
       (lambda ()
         (when (org-at-heading-p)
           (let* ((current-subtree (org-element-at-point))
                  (id (or (org-element-property :name      current-subtree)
                          (org-element-property :ID        current-subtree)
                          (org-element-property :CUSTOM_ID current-subtree)))
                  (level (nth 1 (org-heading-components)))
                  (tags (org-get-tags))
                  (title (or (nth 4 (org-heading-components)) ""))
                  (basename (concat (replace-regexp-in-string " " "-" (downcase (or id title)))
                                    ".md"))
                  (filename (outfile basename))
                  (stored-filename (org-entry-get (point) "EXPORT_FILE_NAME"))
                  (point-in-subtree (<= (org-element-property :begin current-subtree)
                                        original-point
                                        (org-element-property :end current-subtree)))
                  (is-subset (or (equal do-subset "all")
                                 (and (equal do-subset "tagged") (member "subset" tags))
                                 (and (equal do-subset "sample") (member "sample" tags))
                                 (and (equal do-subset "current") point-in-subtree))))
             (fset 'add-to-bookfiles
                   (lambda (line &optional always)
                     (let ((line-n (concat line "\n")))
                       (unless only-subset
                         (append-to-file line-n nil (outfile "Book.txt")))
                       (when (and (not only-subset) (or (member "sample" tags) always))
                         (append-to-file line-n nil (outfile "Sample.txt")))
                       (when (or is-subset always)
                         (append-to-file line-n nil (outfile "Subset.txt"))))))
             (when (= level 1) ;; export only first level entries
               ;; add appropriate tag for front/main/backmatter for tagged headlines
               (dolist (tag matter-tags)
                 (when (member tag tags)
                   (let* ((fname (concat tag ".txt")))
                     (append-to-file (concat "{" tag "}\n") nil (outfile fname))
                     (add-to-bookfiles fname t))))
               ;; add to the filename to Book.txt and to Sample.txt "sample" tag is found.
               (add-to-bookfiles (file-name-nondirectory filename))
               (when (or (not only-subset)
                         is-subset)
                 ;; set filename only if the property is missing or if its value is
                 ;; different from the correct one
                 (or (string= stored-filename filename)
                     (org-entry-put (point) "EXPORT_FILE_NAME" filename))
                 ;; select the subtree so that its headline is also exported
                 ;; (otherwise we get just the body)
                 (org-mark-subtree)
                 (message (format "Exporting %s (%s)" filename title))
                 (org-leanpub-export-to-markdown nil t)))))) "-noexport"))
    (message (format "LeanPub export to %s/ finished" outdir))))
```


## Appearance, buffer/file management and theming {#appearance-buffer-file-management-and-theming}

Here we take care of all the visual, UX and desktop-management settings.

You'll notice that many of the packages in this section have `:defer nil`. This is because some of these package are never called explicitly because they operate in the background, but I want them loaded when Emacs starts so they can perform their necessary customization.

Emacs 26 (which I am trying now) introduces pixel-level scrolling.

```emacs-lisp
(when (>= emacs-major-version 26)
  (pixel-scroll-mode))
```

The `diminish` package makes it possible to remove clutter from the modeline. Here we just load it, it gets enabled for individual packages in their corresponding declarations.

```emacs-lisp
(use-package diminish
  :defer 1)
```

I have been playing with different themes, and I have settled for now in `gruvbox`. Some of my other favorites are also here so I don't forget about them.

```emacs-lisp
;;(use-package solarized-theme)
;;(use-package darktooth-theme)
;;(use-package kaolin-themes)
(use-package gruvbox-theme)
(load-theme 'gruvbox)
```

Install [smart-mode-line](https://github.com/Malabarba/smart-mode-line) for modeline goodness, including configurable abbreviation of directories, and other things.

```emacs-lisp
(use-package smart-mode-line
  :defer 2
  :config
  (sml/setup)
  :custom
  (sml/theme 'dark)
  (sml/replacer-regexp-list
   '(("^~/\\.emacs\\.d/elpa/"                            ":ELPA:")
     ("^~/\\.emacs\\.d/"                                 ":ED:")
     ("^/sudo:.*:"                                       ":SU:")
     ("^~/Documents/"                                    ":Doc:")
     ("^:\\([^:]*\\):Documento?s/"                       ":\\1/Doc:")
     ("^~/Dropbox/"                                      ":DB:")
     ("^:DB:org"                                         ":Org:")
     ("^:DB:Personal/"                                   ":P:")
     ("^:DB:Personal/writing/"                           ":Write:")
     ("^:P:devel/"                                       ":Dev:")
     ("^:Write:learning-cfengine-3/learning-cfengine-3/" ":cf-learn:")
     ("^:Dev:go/src/github.com/elves/elvish/"            ":elvish:")
     ("^:Dev:zzamboni.org/zzamboni.org/"                 ":zz.org:"))))
```

Enable desktop-save mode, which saves the current buffer configuration on exit and reloads it on restart.

```emacs-lisp
(use-package desktop
  :defer nil
  :custom
  (desktop-restore-eager   1   "Restore only the first buffer right away")
  (desktop-lazy-idle-delay 1   "Restore the rest of the buffers 1 seconds later")
  (desktop-lazy-verbose    nil "Be silent about lazily opening buffers")
  :bind
  ("C-M-s-k" . desktop-clear)
  :config
  (desktop-save-mode))
```

The `uniquify` package makes it much easier to identify different open files with the same name by prepending/appending their directory or some other information to them. I configure it to add the directory name after the filename. `uniquify` is included with Emacs, so I specify `:ensure nil` so that `use-package` doesn't try to install it, and just loads and configures it.

```emacs-lisp
(use-package uniquify
  :defer 1
  :ensure nil
  :custom
  (uniquify-after-kill-buffer-p t)
  (uniquify-buffer-name-style 'post-forward)
  (uniquify-strip-common-suffix t))
```

I like to highlight the current line and column. I'm still deciding between two approaches:

-   Using the built-in `global-hl-mode` to always highlight the current line, together with the `col-highlight` package, which highlights the column only after a defined interval has passed
-   Using the `crosshairs` package, which combines both but always highlights both the column and the line. It also has a "highlight crosshairs when idle" mode, but I prefer to have the current line always highlighted, I'm only undecided about the always-on column highlighting.

Sometimes I find the always-highlighted column to be distracting, but other times I find it useful. So I have both pieces of code here, I'm still deciding. Both are disabled for now.

```emacs-lisp
(use-package hl-line
  :disabled
  :defer nil
  :config
  (global-hl-line-mode))
(use-package col-highlight
  :disabled
  :defer nil
  :config
  (col-highlight-toggle-when-idle)
  (col-highlight-set-interval 2))
(use-package crosshairs
  :disabled
  :defer nil
  :config
  (crosshairs-mode))
```

I also use `recentf` to keep a list of recently open buffers. These are visible in helm's open-file mode.

```emacs-lisp
(use-package recentf
  :defer 1
  :custom
  (recentf-max-menu-items 100)
  (recentf-max-saved-items 100)
  :init
  (recentf-mode))
```

The [ibuffer](http://martinowen.net/blog/2010/02/03/tips-for-emacs-ibuffer.html) package allows all sort of useful operations on the list of open buffers. I haven't customized it yet, but I have a keybinding to open it. (Disabled for now as I am using helm's `helm-buffer-list`).

```emacs-lisp
(use-package ibuffer
  :disabled
  :bind
  ("C-x C-b" . ibuffer))
```

The [smex](https://github.com/nonsequitur/smex) package is incredibly useful, adding IDO integration and some other very nice features to `M-x`, which make it easier to discover and use Emacs commands. Highly recommended. (Disabled for now as I'm using helm's `helm-M-x`).

```emacs-lisp
(use-package smex
  :disabled
  :bind (("M-x" . smex))
  :config (smex-initialize))
```

[midnight-mode](https://www.emacswiki.org/emacs/MidnightMode) purges buffers which haven't been displayed in 3 days. We configure the period so that the cleanup happens every 2 hours (7200 seconds).

```emacs-lisp
(use-package midnight
  :defer 3
  :config
  (setq midnight-period 7200)
  (midnight-mode 1))
```

For distraction-free writing, I'm testing out `writeroom-mode`.

```emacs-lisp
(use-package writeroom-mode)
```

[NeoTree](https://github.com/jaypei/emacs-neotree) shows a navigation tree on a sidebar, and allows a number of operations on the files and directories. I'm not much of a fan of this type of interface in Emacs, but I have set it up to check it out.

```emacs-lisp
(use-package neotree
  :config
  (customize-set-variable 'neo-theme (if (display-graphic-p) 'icons 'arrow))
  (customize-set-variable 'neo-smart-open t)
  (customize-set-variable 'projectile-switch-project-action 'neotree-projectile-action)
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
  :bind
  ([f8] . neotree-project-dir))
```

`wc-mode` allows counting characters and words, both on demand and continuously. It also allows setting up a word/character goal.

```emacs-lisp
(use-package wc-mode
  :defer 3)
```

The `all-the-icons` package provides a number of useful icons.

```emacs-lisp
(use-package all-the-icons
  :defer 3)
```


### Completion: IDO or Helm? {#completion-ido-or-helm}

The [battle](https://tuhdo.github.io/helm-intro.html) [rages](https://news.ycombinator.com/item?id=11100312) [on](https://www.reddit.com/r/emacs/comments/3o36sc/what%5Fdo%5Fyou%5Fprefer%5Fido%5For%5Fhelm/) - [helm](https://github.com/emacs-helm/helm) or [IDO](https://www.emacswiki.org/emacs/InteractivelyDoThings)? Both are nice completion frameworks for Emacs, and both integrate nicely with most main Emacs functions, including file opening, command and buffer selection, etc. I was using IDO for some time but are now giving helm a try. Both my configs are shown below, but only Helm is enabled at the moment.

Should I also look at [ivy](https://sam217pa.github.io/2016/09/13/from-helm-to-ivy/)?


#### IDO {#ido}

I use [IDO mode](https://www.masteringemacs.org/article/introduction-to-ido-mode) to get better matching capabilities everywhere in Emacs (disabled while I give helm a try, see below).

```emacs-lisp
(use-package ido
  :disabled
  :config
  (ido-mode t)
  (ido-everywhere 1)
  (setq ido-use-virtual-buffers t)
  (setq ido-enable-flex-matching t)
  (setq ido-use-filename-at-point nil)
  (setq ido-auto-merge-work-directories-length -1))

(use-package ido-completing-read+
  :disabled
  :config
  (ido-ubiquitous-mode 1))
```


#### Helm {#helm}

This config came originally from [Uncle Dave's Emacs config](https://github.com/daedreth/UncleDavesEmacs#user-content-ido-and-why-i-started-using-helm), thought I have tweaked it a bit.

```emacs-lisp
(use-package helm
  :defer 1
  :diminish helm-mode
  :bind
  (("C-x C-f"       . helm-find-files)
   ("C-x C-b"       . helm-buffers-list)
   ("C-x b"         . helm-multi-files)
   ("M-x"           . helm-M-x)
   :map helm-find-files-map
   ("C-<backspace>" . helm-find-files-up-one-level)
   ("C-f"           . helm-execute-persistent-action)
   ([tab]           . helm-ff-RET))
  :config
  (defun daedreth/helm-hide-minibuffer ()
    (when (with-helm-buffer helm-echo-input-in-header-line)
      (let ((ov (make-overlay (point-min) (point-max) nil nil t)))
        (overlay-put ov 'window (selected-window))
        (overlay-put ov 'face
                     (let ((bg-color (face-background 'default nil)))
                       `(:background ,bg-color :foreground ,bg-color)))
        (setq-local cursor-type nil))))
  (add-hook 'helm-minibuffer-set-up-hook 'daedreth/helm-hide-minibuffer)
  (setq helm-autoresize-max-height 0
        helm-autoresize-min-height 40
        helm-M-x-fuzzy-match t
        helm-buffers-fuzzy-matching t
        helm-recentf-fuzzy-match t
        helm-semantic-fuzzy-match t
        helm-imenu-fuzzy-match t
        helm-split-window-in-side-p nil
        helm-move-to-line-cycle-in-source nil
        helm-ff-search-library-in-sexp t
        helm-scroll-amount 8
        helm-echo-input-in-header-line nil)
  :init
  (helm-mode 1))

  (require 'helm-config)
  (helm-autoresize-mode 1)

  (use-package helm-flx
    :custom
    (helm-flx-for-helm-find-files t)
    (helm-flx-for-helm-locate t)
    :config
    (helm-flx-mode +1))
```


## Coding {#coding}

Coding is one of my primary uses for Emacs, although lately it has shifted toward more general writing. This used to be the largest section in my config until [Org mode](#org-mode) overtook it :)


### General settings and modules {#general-settings-and-modules}

When enabled, `subword` allows navigating "sub words" individually in CamelCaseIdentifiers. For now I only enable it in `clojure-mode`.

```emacs-lisp
(use-package subword
  :hook
  (clojure-mode . subword-mode))
```

With `aggressive-indent`, indentation is always kept up to date in the whole buffer. Sometimes it gets in the way, but in general it's nice and saves a lot of work, so I enable it for all programming modes except for Python mode, where I explicitly disable as it often gets the indentation wrong and messes up existing code.

Disabled for now while I test how much I miss it (I often find it gets in the way, but I'm not sure how often it helps and I don't even notice it)

```emacs-lisp
(use-package aggressive-indent
  :disabled
  :diminish aggressive-indent-mode
  :hook
  (prog-mode . aggressive-indent-mode)
  (python-mode . (lambda () (aggressive-indent-mode -1))))
```

With `company-mode`, we get automatic completion - when there are completions available, a popup menu will appear when you stop typing for a moment, and you can either continue typing or accept the completion using the Enter key. I enable it globally.

```emacs-lisp
(use-package company
  :diminish company-mode
  :hook
  (after-init . global-company-mode))
```

`projectile-mode` allows us to perform project-relative operations such as searches, navigation, etc.

```emacs-lisp
(use-package projectile
  :defer 2
  :diminish projectile-mode
  :config
  (projectile-global-mode))
```

I find `iedit` absolutely indispensable when coding. In short: when you hit `Ctrl-:`, all occurrences of the symbol under the cursor (or the current selection) are highlighted, and any changes you make on one of them will be automatically applied to all others. It's great for renaming variables in code.

```emacs-lisp
(use-package iedit
  :custom
  (iedit-toggle-key-default (kbd "C-;"))
  :config
  (set-face-background 'iedit-occurrence "Magenta"))
```

Turn on the online documentation mode for all programming modes (not all of them support it) and for the Clojure REPL `cider` mode.

```emacs-lisp
(use-package eldoc
  :diminish
  :hook
  (prog-mode       . turn-on-eldoc-mode)
  (cider-repl-mode . turn-on-eldoc-mode))
```

On-the-fly spell checking. I enable it for all text modes.

```emacs-lisp
(use-package flyspell
  :defer 1
  :hook (text-mode . flyspell-mode)
  :diminish
  :bind (:map flyspell-mouse-map
              ([down-mouse-3] . #'flyspell-correct-word)
              ([mouse-3]      . #'undefined)))
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
  :custom
  ;; nice pretty printing
  (cider-repl-use-pretty-printing nil)
  ;; nicer font lock in REPL
  (cider-repl-use-clojure-font-lock t)
  ;; result prefix for the REPL
  (cider-repl-result-prefix "; => ")
  ;; never ending REPL history
  (cider-repl-wrap-history t)
  ;; looong history
  (cider-repl-history-size 5000)
  ;; persistent history
  (cider-repl-history-file "~/.emacs.d/cider-history")
  ;; error buffer not popping up
  (cider-show-error-buffer nil)
  ;; go right to the REPL buffer when it's finished connecting
  (cider-repl-pop-to-buffer-on-connect t))
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
  :hook
  (clojure-mode . my-clojure-mode-hook))
```

When coding in LISP-like languages, `rainbow-delimiters` is a must-have - it marks each concentric pair of parenthesis with different colors, which makes it much easier to understand expressions and spot mistakes.

```emacs-lisp
(use-package rainbow-delimiters
  :hook
  ((prog-mode cider-repl-mode) . rainbow-delimiters-mode))
```

Another useful addition for LISP coding - `smartparens` enforces parenthesis to match, and adds a number of useful operations for manipulating parenthesized expressions. I map `M-(` to enclose the next expression as in `paredit` using a custom function. Prefix argument can be used to indicate how many expressions to enclose instead of just 1. E.g. `C-u 3 M-(` will enclose the next 3 sexps.

```emacs-lisp
(defun zz/sp-enclose-next-sexp (num) (interactive "p") (insert-parentheses (or num 1)))
(use-package smartparens
  :diminish smartparens-mode
  :config
  (require 'smartparens-config)
  :custom
  (sp-base-key-bindings 'paredit)
  :hook
  ((clojure-mode
    emacs-lisp-mode
    lisp-mode
    cider-repl-mode
    racket-mode
    racket-repl-mode) . smartparens-strict-mode)
  (smartparens-mode  . sp-use-paredit-bindings)
  (smartparens-mode  . (lambda () (local-set-key (kbd "M-(") 'zz/sp-enclose-next-sexp))))
```

Minor mode for highlighting the current sexp in LISP modes.

```emacs-lisp
(use-package hl-sexp
  :hook
  ((clojure-mode lisp-mode emacs-lisp-mode) . hl-sexp-mode))
```

Trying out [lispy](https://github.com/abo-abo/lispy) for LISP code editing (disabled for now).

```emacs-lisp
(use-package lispy
  :disabled
  :config
  (defun enable-lispy-mode () (lispy-mode 1))
  :hook
  ((clojure-mode
    emacs-lisp-mode
    common-lisp-mode
    scheme-mode
    lisp-mode) . enable-lispy-mode))
```

I am sometimes trying out [parinfer](https://shaunlebron.github.io/parinfer/) (disabled for now).

```emacs-lisp
(use-package parinfer
  :disabled
  :bind
  (("C-," . parinfer-toggle-mode))
  :init
  (setq parinfer-extensions
        '(defaults       ; should be included.
           pretty-parens  ; different paren styles for different modes.
           ;;evil           ; If you use Evil.
           lispy          ; If you use Lispy. With this extension, you should install Lispy and do not enable lispy-mode directly.
           paredit        ; Introduce some paredit commands.
           smart-tab      ; C-b & C-f jump positions and smart shift with tab & S-tab.
           smart-yank))   ; Yank behavior depend on mode.
  :hook
  ((clojure-mode
    emacs-lisp-mode
    common-lisp-mode
    scheme-mode
    lisp-mode) . parinfer-mode))
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

-   Build and check MELPA package definitions

    ```emacs-lisp
    (use-package package-build)
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

-   Use `helm-pass` as an interface to `pass`.

    ```emacs-lisp
    (use-package helm-pass)
    ```

-   git interface with some simple configuration I picked up somewhere. When you press <kbd>C-c C-g</kbd>, `magit-status` runs full-screen, but when you press <kbd>q</kbd>, it restores your previous window setup. Very handy.

    ```emacs-lisp
    (use-package magit
      :diminish auto-revert-mode
      :bind
      (("C-c C-g" . magit-status)
       :map magit-status-mode-map
       ("q"       . magit-quit-session))
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
        (jump-to-register :magit-fullscreen)))
    ```

-   Interface to use the [silver-searcher](https://geoff.greer.fm/ag/)

    ```emacs-lisp
    (use-package ag)
    ```

-   Publishing with [Hugo](https://gohugo.io/). I don't use this anymore since I started [blogging with ox-hugo](#blogging-with-hugo). I keep it loaded, but without its keybinding, because it makes it easy sometimes to see the history of my Markdown posts.

    ```emacs-lisp
    (use-package easy-hugo
      :custom
      (easy-hugo-basedir "~/Personal/devel/zzamboni.org/zzamboni.org/")
      (easy-hugo-url "http://zzamboni.org/")
      (easy-hugo-previewtime "300")
      ;;(define-key global-map (kbd "C-c C-e") 'easy-hugo)
      )
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

-   [auto-insert mode](https://www.gnu.org/software/emacs/manual/html%5Fnode/autotype/Autoinserting.html) for automatically inserting user-defined templates for certain file types. It's included with Emacs, so I just configure its directory to one inside my Dropbox, and set the hook to run it automatically when opening a file.

    ```emacs-lisp
    (use-package autoinsert
      :ensure nil
      :custom
      (auto-insert-directory (concat user-emacs-directory "auto-insert/"))
      :hook
      (find-file . auto-insert))
    ```

-   Create and manage [GitHub gists](https://gist.github.com/). Setting `gist-view-gist` to `t` makes it open new gists in the web browser automatically after creating them.

    ```emacs-lisp
    (use-package gist
      :custom
      (gist-view-gist t "Automatically open new gists in browser"))
    ```

-   [Emacs Startup Profiler](https://github.com/jschaf/esup), to get detailed stats of what's taking time during initialization.

    ```emacs-lisp
    (use-package esup)
    ```

-   Macro to measure how long a command takes, from <https://stackoverflow.com/questions/23622296/emacs-timing-execution-of-function-calls-in-emacs-lisp>

```emacs-lisp
(defmacro measure-time (&rest body)
  "Measure the time it takes to evaluate BODY."
  `(let ((time (current-time)))
     ,@body
     (message "%.06f" (float-time (time-since time)))))
```


## General text editing {#general-text-editing}

In addition to coding, I configure some modes that can be used for text editing.

-   [AsciiDoc](http://asciidoctor.org/docs/user-manual/), which I use for [my book](http://cf-learn.info/) and some other text. I also set up `visual-line-mode` and `variable-pitch-mode` here. `adoc-mode` is not so granular as `org-mode` with respect to face assignments, so the variable/fixed distinction does not always work, but it's still pretty good for long-text editing.

    ```emacs-lisp
    (use-package adoc-mode
      :mode "\\.asciidoc\\'"
      :hook
      (adoc-mode . visual-line-mode)
      (adoc-mode . variable-pitch-mode))
    ```

-   [Markdown](https://daringfireball.net/projects/markdown/syntax), generally useful. I also set up variable pitch and visual line mode.

    ```emacs-lisp
    (use-package markdown-mode
      :hook
      (markdown-mode . visual-line-mode)
      (markdown-mode . variable-pitch-mode))
    ```

-   When [typopunct](https://www.emacswiki.org/emacs/TypographicalPunctuationMarks) is enabled (needs to be enabled by hand), automatically inserts “pretty” quotes of the appropriate type.

    ```emacs-lisp
    (use-package typopunct
      :config
      (typopunct-change-language 'english t))
    ```


## Cheatsheet and experiments {#cheatsheet-and-experiments}

Playground and how to do different things, not necessarily used in my Emacs config but useful sometimes.

This is how we get a global header property in org-mode

```emacs-lisp
(alist-get :tangle
           (org-babel-parse-header-arguments
            (org-entry-get-with-inheritance "header-args")))
```

Testing formatting org snippets to look like noweb-rendered output.

```emacs-lisp
(customize-set-variable 'org-entities-user
                        '(("llangle" "\\llangle" t "&lang;&lang;" "<<" "<<" "《")
                          ("rrangle" "\\rrangle" t "&rang;&rang;" ">>" ">>" "》")))
(setq org-babel-exp-code-template
      (concat "\n@@latex:\\noindent@@\\llangle​//​\\rrangle\\equiv\n"
              org-babel-exp-code-template))
```

An experiment to reduce file tangle time, from <https://www.wisdomandwonder.com/article/10630/how-fast-can-you-tangle-in-org-mode>. In my tests it doesn't have a noticeable impact.

```emacs-lisp
(setq help/default-gc-cons-threshold gc-cons-threshold)
(defun help/set-gc-cons-threshold (&optional multiplier notify)
  "Set `gc-cons-threshold' either to its default value or a
   `multiplier' thereof."
  (let* ((new-multiplier (or multiplier 1))
         (new-threshold (* help/default-gc-cons-threshold
                           new-multiplier)))
    (setq gc-cons-threshold new-threshold)
    (when notify (message "Setting `gc-cons-threshold' to %s"
                          new-threshold))))
(defun help/double-gc-cons-threshold () "Double `gc-cons-threshold'." (help/set-gc-cons-threshold 10))
(add-hook 'org-babel-pre-tangle-hook #'help/double-gc-cons-threshold)
(add-hook 'org-babel-post-tangle-hook #'help/set-gc-cons-threshold)
```


## Epilogue {#epilogue}

Here we close the `let` expression from [the preface](#performance-optimization).

```emacs-lisp
)
```

We also reset the value of `gc-cons-threshold`, not to its original value, we still leave it larger than default so that GCs don't happen so often.

```emacs-lisp
(setq gc-cons-threshold (* 2 1000 1000))
```
