+++
title = "My Emacs Configuration, With Commentary"
author = ["Diego Zamboni"]
summary = "I have enjoyed slowly converting my configuration files to literate programming style using org-mode in Emacs. It's now the turn of my Emacs configuration file."
date = 2017-12-17T20:14:00+01:00
tags = ["config", "howto", "literateprogramming", "literateconfig", "emacs"]
draft = false
creator = "Emacs 26.3 (Org mode 9.2.6 + ox-hugo)"
featured_image = "/images/emacs-logo.svg"
toc = true
+++

{{< leanpubbook book="lit-config" style="float:right" >}}

Last update: **November 19, 2019**

I have enjoyed slowly converting my configuration files to [literate programming](http://www.howardism.org/Technical/Emacs/literate-programming-tutorial.html) style style using org-mode in Emacs. I previously posted my [Elvish configuration](../my-elvish-configuration-with-commentary/), and now it's the turn of my Emacs configuration file. The text below is included directly from my [init.org](https://github.com/zzamboni/dot%5Femacs/blob/master/init.org) file. Please note that the text below is a snapshot as the file stands as of the date shown above, but it is always evolving. See the [init.org file in GitHub](https://github.com/zzamboni/dot%5Femacs/blob/master/init.org) for my current, live configuration, and the generated file at [init.el](https://github.com/zzamboni/dot%5Femacs/blob/master/init.el).

If you are interested in writing your own Literate Config files, check out my new book [Literate Config](https://leanpub.com/lit-config) on Leanpub!


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

First, a hook that reports how long and how many garbage collections the startup took. We use a hook to run it at the very end, so the message doesn't get clobbered by other messages during startup.

```emacs-lisp
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

Optionally enable `debug-on-error` - I do this only when I'm trying to figure out some problem in my config.

```emacs-lisp
;;(setq debug-on-error t)
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

My current `custom.el` file can be  found  at <https://github.com/zzamboni/dot-emacs/blob/master/custom.el>.


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
                        '(("marmalade" . "https://marmalade-repo.org/packages/")
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

-   The `use-package-verbose` variable enables verbose loading of packages, useful for debugging. I set/unset this according to need.

    ```emacs-lisp
    (customize-set-variable 'use-package-verbose nil)
    ```

Testing [`quelpa`](https://framagit.org/steckerhalter/quelpa) and to install packages directly from their github repositories (and other places). I install `quelpa` using `use-package` first, and then install [`quelpa-use-package`](https://framagit.org/steckerhalter/quelpa-use-package) to allow using `quelpa` from  within `use-package` declarations. Very recursive.

```emacs-lisp
(use-package quelpa
  :defer nil)

(use-package quelpa-use-package
  :defer nil
  :after quelpa)
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

Giving a try to [Paradox](https://github.com/Malabarba/paradox) for an enhanced package management interface. We set `paradox-github-token` to `t` to disable GitHub integration (I don't want to star  repos).

```emacs-lisp
(use-package paradox
  :defer nil
  :custom
  (paradox-github-token t)
  :config
  (paradox-enable))
```


## Settings {#settings}


### Proxy settings {#proxy-settings}

These are two short functions I wrote to be able to set/unset proxy settings within Emacs. I haven't bothered to improve or automate this, as I pretty much only need it to be able to install packages sometimes when I'm at work. For now I just call them manually with `M-x zz/(un)set-proxy` when I need to.

```emacs-lisp
(defun zz/set-proxy ()
  (interactive)
  (customize-set-variable 'url-proxy-services
                          '(("http"  . "proxy.corproot.net:8079")
                            ("https" . "proxy.corproot.net:8079"))))
(defun zz/unset-proxy ()
  (interactive)
  (customize-set-variable 'url-proxy-services nil))
```


### Miscellaneous settings {#miscellaneous-settings}

-   Load the `cl` library to enable some additional macros (e.g. `lexical-let`).

    ```emacs-lisp
    (require 'cl)
    ```

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

-   Show line numbers. I used `linum-mode` before, but it caused severe performance issues on large files. Emacs 26 introduces `display-line-numbers-mode`, which has no perceivable performance impact even on very large files. Disabled for now.

    ```emacs-lisp
    (when (>= emacs-major-version 26)
      (use-package display-line-numbers
        :defer nil
        :ensure nil
        :config
        (global-display-line-numbers-mode)))
    ```

-   Highlight trailing whitespace in red, so it's easily visible (disabled  for now as it created a lot of noise in some modes, e.g. the org-mode export screen)

    ```emacs-lisp
    (customize-set-variable 'show-trailing-whitespace nil)
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
    (customize-set-variable
     'backup-directory-alist
     `(("." . ,(concat user-emacs-directory "backups"))))
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

The [which-key](https://github.com/justbur/emacs-which-key) package makes Emacs functionality much easier to discover and explore: in short, after you start the input of a command and stop, pondering what key must follow, it will automatically open a non-intrusive buffer at the bottom of the screen offering you suggestions for completing the command. Extremely useful.

```emacs-lisp
(use-package which-key
  :defer nil
  :diminish which-key-mode
  :config
  (which-key-mode))
```

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
      ("C-S-s" . vr/isearch-forward)
      ("C-M-s" . isearch-forward)
      ("C-M-r" . isearch-backward))
    ```

-   Key binding to use "[hippie expand](http://www.emacswiki.org/emacs/HippieExpand)" for text autocompletion

    ```emacs-lisp
    (bind-key "M-/" 'hippie-expand)
    ```


### Emulating vi's `%` key {#emulating-vi-s-key}

One of the few things I missed in Emacs from vi was the `%` key, which jumps to the parenthesis, bracket or brace which matches the one below the cursor. This function implements the functionality. Inspired by <http://www.emacswiki.org/emacs/NavigatingParentheses>, but modified to use `smartparens` instead of the default commands, and to work on brackets and braces.

```emacs-lisp
(defun zz/goto-match-paren (arg)
  "Go to the matching paren/bracket, otherwise (or if ARG is not
  nil) insert %.  vi style of % jumping to matching brace."
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

I use `use-package` to load the `org` package, and put its configuration inside the corresponding sections for keybindings (`:bind`), custom variables (`:custom`), custom faces (`:custom-face`), hooks (`:hook`) and general configuration code (`:config`), respectively. The contents of each section is populated with the corresponding snippets that follow. See the sections below for the details on what goes into each configuration section, and some other configuration code that ends up outside this declaration.

```emacs-lisp
(use-package org
  :pin manual
  :load-path ("lisp/org-mode/lisp" "lisp/org-mode/lisp/contrib/lisp")
  :bind
    <<org-mode-keybindings>>
  :custom
    <<org-mode-custom-vars>>
  :custom-face
    <<org-mode-faces>>
  :hook
    <<org-mode-hooks>>
  :config
    <<org-mode-config>>)
```


### General Org Configuration {#general-org-configuration}

Note that mode-specific configuration variables are defined under  their corresponding packages, this  section defines only global org-mode configuration variables, which are inserted in the main `use-package` declaration for `org-mode`.

-   Default directory for org files (not all are stored here).

    ```emacs-lisp
    (org-directory "~/Dropbox/Personal/org")
    ```

-   Automatically log done times in todo items.

    ```emacs-lisp
    (org-log-done t)
    ```

-   Keep the indentation well structured by setting `org-startup-indented` to `t`. This is a must have. Makes it feel less like editing a big text file and more like a purpose built editor for org-mode that forces the indentation. Thanks [Nick](https://github.com/nickanderson/Level-up-your-notes-with-Org/blob/master/Level-up-your-notes-with-Org.org#automatic-visual-indention) for the tip!

    ```emacs-lisp
    (org-startup-indented t)
    ```

    By default, `org-indent` produces an indicator `"Ind"` in the modeline. We use diminish to hide it. I also like to increase  the indentation a bit so that  the levels are more visible.

    ```emacs-lisp
    (use-package org-indent
      :ensure nil
      :diminish
      :custom
      (org-indent-indentation-per-level 4))
    ```

-   Log stuff into the LOGBOOK drawer by default

    ```emacs-lisp
    (org-log-into-drawer t)
    ```


### General Org  Keybindings {#general-org-keybindings}

Note that other keybindings are configured under their corresponding packages, this section defines only global org-mode keybindings, which are inserted in the main `use-package` declaration for `org-mode`.

-   Set up `C-c l` to store a link to the current org object, in counterpart to the default `C-c C-l` to insert a link.

    ```emacs-lisp
    ("C-c l" . org-store-link)
    ```

-   The default keybinding for `org-mark-element` is `M-h`, which in macOS hides the current application, so I bind it to `A-h`.

    ```emacs-lisp
    ("A-h" . org-mark-element)
    ```

Enable [Speed Keys](https://orgmode.org/manual/Speed-keys.html), which allows quick single-key commands when the cursor is placed on a heading. Usually the cursor needs to be at the beginning of a headline line, but defining it with this function makes them active on any of the asterisks at the beginning of the line (useful with the [font highlighting I use](#beautifying-org-mode), as all but the last asterisk are sometimes not visible).

```emacs-lisp
(org-use-speed-commands
 (lambda ()
   (and (looking-at org-outline-regexp)
        (looking-back "^\**"))))
```


### Task tracking {#task-tracking}

Org-Agenda is the umbrella for all todo, journal, calendar, and other views. I set up `C-c a` to call up agenda mode.

```emacs-lisp
(use-package org-agenda
  :ensure nil
  :after org
  :bind
  ("C-c a" . org-agenda)
  :custom
  (org-agenda-include-diary t)
  (org-agenda-prefix-format '((agenda . " %i %-12:c%?-12t% s")
                              ;; Indent todo items by level to show nesting
                              (todo . " %i %-12:c%l")
                              (tags . " %i %-12:c")
                              (search . " %i %-12:c")))
  (org-agenda-start-on-weekday nil))
```

I also provide some customization for the `holidays` package, since its entries are included in the Org Agenda through the `org-agenda-include-diary` integration.

```emacs-lisp
(use-package mexican-holidays
  :defer nil)
```

```emacs-lisp
(quelpa '(swiss-holidays :fetcher github :repo "egli/swiss-holidays"))
(require 'swiss-holidays)
```

```emacs-lisp
(use-package holidays
  :defer nil
  :ensure nil
  :init
  (require 'mexican-holidays)
  :config
  (setq calendar-holidays
        (append '((holiday-fixed 1 1 "New Year's Day")
                  (holiday-fixed 2 14 "Valentine's Day")
                  (holiday-fixed 4 1 "April Fools' Day")
                  (holiday-fixed 10 31 "Halloween")
                  (holiday-easter-etc)
                  (holiday-fixed 12 25 "Christmas")
                  (solar-equinoxes-solstices))
                swiss-holidays
                swiss-holidays-catholic
                swiss-holidays-zh-city-holidays
                holiday-mexican-holidays)))
```

[`org-super-agenda`](https://github.com/alphapapa/org-super-agenda) provides great grouping and customization features to make agenda mode easier to use.

```emacs-lisp
(require 'org-habit)
(use-package org-super-agenda
  :custom
  (org-super-agenda-groups '((:auto-dir-name t))))
```

I configure `org-archive` to archive completed TODOs by default to the `archive.org` file in the same directory as the source file, under the "date tree" corresponding to the task's CLOSED date - this allows me to easily separate work from non-work stuff. Note that this can be overridden for specific files by specifying the desired value of `org-archive-location` in the `#+archive:` property at the top of the file.

```emacs-lisp
(use-package org-archive
  :ensure nil
  :custom
  (org-archive-location "archive.org::datetree/"))
```


### Capturing  stuff {#capturing-stuff}

First, I define some global keybindings  to open my frequently-used org files (original tip from [Learn how to take notes more efficiently in Org Mode](https://sachachua.com/blog/2015/02/learn-take-notes-efficiently-org-mode/)).

I define a helper function to define keybindings that open files. Since I use the `which-key` package, it also defines the description of the key that will appear in the `which-key` menu. Note the use of `lexical-let` so that  the `lambda` creates a closure, otherwise the keybindings don't work.

```emacs-lisp
(defun zz/add-file-keybinding (key file &optional desc)
  (lexical-let ((key key)
                (file file)
                (desc desc))
    (global-set-key (kbd key) (lambda () (interactive) (find-file file)))
    (which-key-add-key-based-replacements key (or desc file))))
```

Now I define keybindings to access my commonly-used org files.

```emacs-lisp
(zz/add-file-keybinding "C-c f w" "~/Work/work.org.gpg" "work.org")
(zz/add-file-keybinding "C-c f p" "~/org/projects.org" "projects.org")
(zz/add-file-keybinding "C-c f i" "~/org/ideas.org" "ideas.org")
(zz/add-file-keybinding "C-c f d" "~/org/diary.org" "diary.org")
```

`org-capture` provides  a generic and extensible interface  to capturing things  into org-mode in  different formats. I set up <kbd>C-c c</kbd>  as the default  keybinding for triggering `org-capture`. Usually setting up a new capture template requires  some custom code,  which  gets defined in  the corresponding package config sections and included in the `:config` section below.

```emacs-lisp
(use-package org-capture
  :ensure nil
  :after org
  :defer 1
  :bind
  ("C-c c" . org-capture)
  :config
  <<org-capture-config>>
  )
```


### Building presentations {#building-presentations}

[org-reveal](https://github.com/yjwen/org-reveal) is an awesome package for building presentations with org-mode. The MELPA version of the package gives me a conflict with my hand-installed version of org-mode, so I also install it by hand and load it directly from its checked-out repository.

```emacs-lisp
(use-package ox-reveal
  :load-path ("lisp/org-reveal")
  :defer 3
  :after org
  :custom
  (org-reveal-note-key-char nil)
  (org-reveal-root "file:///Users/taazadi1/.emacs.d/lisp/reveal.js"))
(use-package htmlize
  :defer 3
  :after ox-reveal)
```


### Various exporters {#various-exporters}

One of the big strengths of org-mode is the ability to export a document in many different formats. Here I load some of the exporters I have found useful.

-   HTML

    ```emacs-lisp
    (use-package ox-html
      :ensure nil
      :defer 3
      :after org
      :custom
      (org-html-checkbox-type 'unicode))
    ```

-   Markdown

    ```emacs-lisp
    (use-package ox-md
      :ensure nil
      :defer 3
      :after org)
    ```

-   [GitHub Flavored Markdown](https://help.github.com/categories/writing-on-github/)

    ```emacs-lisp
    (use-package ox-gfm
      :defer 3
      :after org)
    ```

-   [Jira markup](https://github.com/stig/ox-jira.el). I also load `org-jira`, which provides a full interface to Jira through org-mode.

    ```emacs-lisp
    (use-package ox-jira
      :defer 3
      :after org)
    ```

    ```emacs-lisp
    (use-package org-jira
      :defer 3
      :after org
      :custom
      (jiralib-url "https://jira.work.com"))
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

<!--listend-->

-   Some customizations for the LaTeX exporter. `ox-latex` gets loaded automatically, but we use `use-package` anyway so that the config code is only executed after the package is loaded. I add a pseudo-class which uses the document class `book` but without parts (only chapters at the top level).

    ```emacs-lisp
    (use-package ox-latex
      :load-path "lisp/org-mode/lisp"
      :ensure nil
      :demand
      :after org
      :custom
      (org-latex-compiler "xelatex")
      (org-latex-pdf-process
       '("%latex -shell-escape -interaction nonstopmode -output-directory %o %f"
         "%latex -interaction nonstopmode -output-directory %o %f"
         "%latex -interaction nonstopmode -output-directory %o %f"))
      :config
      (setq org-latex-listings 'minted)
      (add-to-list 'org-latex-packages-alist '("newfloat" "minted"))
      (add-to-list 'org-latex-minted-langs '(lua "lua"))
      (add-to-list 'org-latex-minted-langs '(shell "shell"))
      (add-to-list 'org-latex-classes
                   '("book-no-parts" "\\documentclass[11pt,letterpaper]{book}"
                     ("\\chapter{%s}" . "\\chapter*{%s}")
                     ("\\section{%s}" . "\\section*{%s}")
                     ("\\subsection{%s}" . "\\subsection*{%s}")
                     ("\\subsubsection{%s}" . "\\subsubsection*{%s}")
                     ("\\paragraph{%s}" . "\\paragraph*{%s}")))
      (add-to-list 'org-latex-classes
                   '("awesome-cv" "\\documentclass{awesome-cv}"
                     ("\\cvsection{%s}" . "\\cvsection{%s}")
                     ("\\cvsubsection{%s}" . "\\cvsubsection{%s}")
                     ("\\subsection{%s}" . "\\subsection*{%s}")
                     ("\\subsubsection{%s}" . "\\subsubsection*{%s}")
                     ("\\cvparagraph{%s}" . "\\cvparagraph{%s}")))
      ;; Necessary for LuaLaTeX to work - see
      ;; https://tex.stackexchange.com/a/374391/10680
      (setenv "LANG" "en_US.UTF-8"))
    ```

-   [ox-clip](https://github.com/jkitchin/ox-clip) to export HTML-formatted snippets.

    ```emacs-lisp
    (use-package ox-clip
      :bind
      ("A-C-M-k" . ox-clip-formatted-copy))
    ```


### Blogging with Hugo {#blogging-with-hugo}

[ox-hugo](https://ox-hugo.scripter.co/) is an awesome way to blog from org-mode. It makes it possible for posts in org-mode format to be kept separate, and it generates the Markdown files for Hugo. Hugo [supports org files](https://gohugo.io/content-management/formats/), but using ox-hugo has multiple advantages:

-   Parsing is done by org-mode natively, not by an external library. Although goorgeous (used by Hugo) is very good, it still lacks in many areas, which leads to text being interpreted differently as by org-mode.
-   Hugo is left to parse a native Markdown file, which means that many of its features such as shortcodes, TOC generation, etc., can still be used on the generated file.
-   I am intrigued by ox-hugo's "one post per org subtree" proposed structure. So far I've always had one file per post, but with org-mode's structuring features, it might make sense to give it a try.

<!--listend-->

```emacs-lisp
(use-package ox-hugo
  :defer 3
  :after org
  ;; Testing hooks to automatically set the filename on an ox-hugo
  ;; blog entry when it gets marked as DONE
  ;; :hook
  ;; (org-mode . (lambda ()
  ;;               (add-hook 'org-after-todo-state-change-hook
  ;;                         (lambda ()
  ;;                           (org-set-property
  ;;                            "testprop"
  ;;                            (concat "org-state: " org-state
  ;;                                    " prev-state: " (org-get-todo-state))))
  ;;                         'run-at-end 'only-in-org-mode)))
  )
```

Configure a capture template for creating new ox-hugo blog posts, from [ox-hugo's Org Capture Setup](https://ox-hugo.scripter.co/doc/org-capture-setup).

```emacs-lisp
(defun org-hugo-new-subtree-post-capture-template ()
  "Returns `org-capture' template string for new Hugo post.
See `org-capture-templates' for more information."
  (let* ((title (read-from-minibuffer "Post Title: "))
         (fname (org-hugo-slug title)))
    (mapconcat #'identity
               `(,(concat "* TODO " title)
                 ":PROPERTIES:"
                 ,(concat ":EXPORT_HUGO_BUNDLE: " fname)
                 ":EXPORT_FILE_NAME: index"
                 ":END:"
                 "%?\n") ; Place the cursor here finally
               "\n")))
(add-to-list 'org-capture-templates
             '("z"       ;`org-capture' binding + z
               "zzamboni.org post"
               entry
               ;; It is assumed that below file is present in `org-directory'
               ;; and that it has an "Ideas" heading. It can even be a
               ;; symlink pointing to the actual location of all-posts.org!
               (file+olp "zzamboni.org" "Ideas")
               (function org-hugo-new-subtree-post-capture-template)))
```


### Encryption {#encryption}

First, load the built-in EasyPG support. By calling `(epa-file-enable)`, Emacs automatically encrypts/decrypts files with a `.gpg` extension. By default it asks about the key to use, but I configure it to always use my own GPG key.

```emacs-lisp
(use-package epa-file
  :ensure nil ;; included with Emacs
  :config
  (setq epa-file-encrypt-to '("diego@zzamboni.org"))
  (epa-file-enable)
  :custom
  (epa-file-select-keys 'silent))
```

Then, load [org-crypt](https://orgmode.org/worg/org-tutorials/encrypting-files.html) to enable selective  encryption/decryption using GPG within org-mode.

```emacs-lisp
(use-package org-crypt
  :ensure nil  ;; included with org-mode
  :after org
  :config
  (org-crypt-use-before-save-magic)
  (setq org-tags-exclude-from-inheritance (quote ("crypt")))
  :custom
  (org-crypt-key "diego@zzamboni.org"))
```


### Keeping a Journal {#keeping-a-journal}

I use [750words](http://750words.com/) for my personal Journal, and I used  to write my entries locally using Scrivener. Now I am using  `org-journal` for this, works quite well  together with `wc-mode` to keep  a count of how many words I have written.

In order to keep my journal entries encrypted there are two separate but confusingly named mechanisms:

-   `org-journal-encrypt-journal`, if set to `t` has the effect of transparently encrypting/decrypting the journal files as they are written to disk. This is what  I use.
-   `org-journal-enable-encryption`, if set to `t`, enables integration with `org-crypt` (see above),  so it automatically adds a `:crypt:` tag to new journal entries. This has the effect of automatically encrypting those entries upon save, replacing them with a blob of gpg-encrypted text which has to be further decrypted with `org-decrypt-entry` in order to read or edit them again. I have disabled it for now to make it more transparent to  work with my journal entries while   I am editing them.

<!--listend-->

```emacs-lisp
(use-package org-journal
  :after org
  :custom
  (org-journal-dir (concat (file-name-as-directory org-directory) "journal"))
  (org-journal-file-format "%Y/%m/%Y%m%d")
  (org-journal-date-format "%A, %Y-%m-%d")
  (org-journal-encrypt-journal t)
  (org-journal-enable-encryption nil)
  (org-journal-enable-agenda-integration t)
  :bind
  ("C-c j" . org-journal-new-entry))
```


### Literate programming {#literate-programming}

Org-mode is the first literate programming tool that seems practical and useful, since it's easy to edit, execute and document code from within the same tool (Emacs) using all of its existing capabilities (i.e. each code block can be edited in its native Emacs mode, taking full advantage of indentation, completion, etc.)

First, we load the necessary programming language support. The base features and literate programming for Emacs LISP is built-in, but the `ob-*` packages provide the ability to execute code in different languages directly from within the Org buffer, beyond those included with org-mode. I load the modules for some of the languages I use frequently:

-   CFEngine, used extensively for my book [_Learning CFEngine_](https://cf-learn.info).

    ```emacs-lisp
    (use-package ob-cfengine3
      :after org)
    ```

-   Elvish, my favorite shell.

    ```emacs-lisp
    (use-package ob-elvish
      :after org)
    ```

-   The [PlantUML](http://plantuml.com/) graph language.

    We determine the location of the PlantUML jar file automatically from the installed Homebrew formula.

    <a id="code-snippet--plantuml-jar-path"></a>
    ```shell
    brew list plantuml | grep jar
    ```

Which in my current setup results in the following:

The command defined above is used to define the value of the `homebrew-plantuml-jar-path` variable. If you don't use Homebrew of have installed PlantUML some other way, you need to modify this command, or hard-code the path.

```emacs-lisp
(require 'subr-x)
(setq homebrew-plantuml-jar-path
      (expand-file-name
       (string-trim
        (shell-command-to-string "brew list plantuml | grep jar"))))
```

Finally, we use this value to configure both `plantuml-mode` (for syntax highlighting) and `ob-plantuml` (for evaluating PlantUML code and inserting the results in exported Org documents).

```emacs-lisp
(use-package plantuml-mode
  :custom
  (plantuml-jar-path homebrew-plantuml-jar-path))

(use-package ob-plantuml
  :ensure nil
  :after org
  :custom
  (org-plantuml-jar-path homebrew-plantuml-jar-path))
```

-   Define `shell-script-mode` as an alias for `console-mode`, so that `console` src blocks can be edited and are fontified correctly.

    ```emacs-lisp
    (defalias 'console-mode 'shell-script-mode)
    ```

-   Finally, from all  the available languages, we configure the  ones for which to load `org-babel` support.

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
       (calc      . t)
       (dot       . t)
       (ditaa     . t)))
    ```

Now, we configure some other `org-babel` settings:

-   This little snippet has revolutionized my literate programming workflow. It automatically runs `org-babel-tangle` upon saving any org-mode buffer, which means the resulting files will be automatically kept up to date.

    ```emacs-lisp
    (org-mode . (lambda () (add-hook 'after-save-hook 'org-babel-tangle
                                     'run-at-end 'only-in-org-mode)))
    ```

-   This is potentially dangerous: it suppresses the query before executing code from within org-mode. I use it because I am very careful and only press `C-c C-c` on blocks I absolutely understand.

    ```emacs-lisp
    (org-confirm-babel-evaluate nil)
    ```

-   This makes it so that code within `src` blocks is fontified according to their corresponding Emacs mode, making the file much more readable.

    ```emacs-lisp
    (org-src-fontify-natively t)
    ```

-   In principle this makes it so that indentation in `src` blocks works as in their native mode, but in my experience it does not always work reliably. For full proper indentation, always edit the code in a native buffer by pressing `C-c '`.

    ```emacs-lisp
    (org-src-tab-acts-natively t)
    ```

-   Automatically show inline images, useful when executing code that produces them, such as PlantUML or Graphviz.

    ```emacs-lisp
    (org-babel-after-execute . org-redisplay-inline-images)
    ```

-   I add hooks to measure and report how long the tangling took. I first define a function to compute and report the elapsed time:

    ```emacs-lisp
    (defun zz/report-tangle-time (start-time)
      (message "org-babel-tangle took %s"
               (format "%.2f seconds"
                       (float-time (time-since start-time)))))
    ```

    And this function is used in the corresponding hooks before and after `org-babel-tangle`:

    ```emacs-lisp
    (org-babel-pre-tangle  . (lambda ()
                               (setq zz/pre-tangle-time (current-time))))
    (org-babel-post-tangle . (lambda ()
                               (zz/report-tangle-time zz/pre-tangle-time)))
    ```


### Beautifying org-mode {#beautifying-org-mode}

These settings make org-mode much more readable by using different fonts for headings, hiding some of the markup, etc. This was taken originally from Howard Abrams' [Org as a Word Processor](http://www.howardism.org/Technical/Emacs/orgmode-wordprocessor.html), and subsequently tweaked and broken up in the different parts of the `use-package` declaration by me.

First, we set `org-hid-emphasis-markers` so that the markup indicators are not shown.

```emacs-lisp
(org-hide-emphasis-markers t)
```

We add an entry to the org-mode font-lock table so that list markers are shown with a middle dot instead of the original character.

```emacs-lisp
(font-lock-add-keywords
 'org-mode
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
              (nil (warn "Cannot find a Sans Serif Font."))))
       (base-font-color (face-foreground 'default nil 'default))
       (headline `(:inherit default :weight bold
                            :foreground ,base-font-color)))

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
   `(org-headline-done  ((t (,@headline ,@variable-tuple :strike-through t))))
   `(org-document-title ((t (,@headline ,@variable-tuple
                                        :height 2.0 :underline nil))))))
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

-   Configure `org-indent` to inherit from `fixed-pitch` to fix the vertical spacing in code blocks. Thanks to Ben for the tip!

    ```emacs-lisp
    (org-indent ((t (:inherit (org-hide fixed-pitch)))))
    ```

-   Configure `org-fontify-done-headline` to apply a special face to DONE items in org-mode, and configure the `org-done` face to be used.  Note that  `org-done` only applies to the "DONE" keyword itself, the face for the rest of a "done" headline is defined above as the `org-headline-done` face.

    ```emacs-lisp
    (org-fontify-done-headline t)
    ```

    ```emacs-lisp
    (org-done ((t (:foreground "PaleGreen"
                               :strike-through t))))
    ```

-   Configuring the corresponding `org-mode` faces for blocks, verbatim code, and maybe a couple of other things. As these change more frequently, I do them directly from the `customize-face` interface, you can see their current settings in the [Customized variables](#customized-variables) section.

-   Setting up `visual-line-mode` and making all my paragraphs one single line, so that the lines wrap around nicely in the window according to their proportional-font size, instead of at a fixed character count, which does not work so nicely when characters have varying widths. I set up a hook that automatically enables `visual-line-mode` and `variable-pitch-mode` when entering org-mode.

    ```emacs-lisp
    (org-mode . visual-line-mode)
    (org-mode . variable-pitch-mode)
    ```

-   In `variable-pitch` mode, the default right-alignment for headline tags doesn't work, and results in the tags being misaligned (as it uses character positions to do the alignment). This setting positions the tags right after the last character of the headline, so at least they are more consistent.

    ```emacs-lisp
    (org-tags-column 0)
    ```

-   I also set `org-todo-keyword-faces` to highlight different  types of org-mode TODO items with different colors.

    ```emacs-lisp
    (org-todo-keyword-faces
     '(("AREA"         . "DarkOrchid1")
       ("[AREA]"       . "DarkOrchid1")
       ("INBOX"        . "cyan")
       ("[INBOX]"      . "cyan")
       ("PROPOSAL"     . "orange")
       ("[PROPOSAL]"   . "orange")
       ("DRAFT"        . "yellow")
       ("[DRAFT]"      . "yellow")
       ("INPROGRESS"   . "yellow")
       ("[INPROGRESS]" . "yellow")
       ("MEETING"      . "purple")
       ("[MEETING]"    . "purple")
       ("CANCELED"     . "blue")
       ("[CANCELED]"   . "blue")))
    ```

    These two modes produce modeline indicators, which I disable using `diminish`.

    ```emacs-lisp
    (eval-after-load 'face-remap '(diminish 'buffer-face-mode))
    (eval-after-load 'simple '(diminish 'visual-line-mode))
    ```

-   Prettify checkbox lists - courtesy of <https://blog.jft.rocks/emacs/unicode-for-orgmode-checkboxes.html>. First, we add special characters for checkboxes:

    ```emacs-lisp
    (org-mode . (lambda ()
                  "Beautify Org Checkbox Symbol"
                  (push '("[ ]" . "☐" ) prettify-symbols-alist)
                  (push '("[X]" . "☑" ) prettify-symbols-alist)
                  (push '("[-]" . "⊡" ) prettify-symbols-alist)
                  (prettify-symbols-mode)))
    ```

    Second, we define a special face for checked items.

    ```emacs-lisp
    (defface org-checkbox-done-text
      '((t (:foreground "#71696A" :strike-through t)))
      "Face for the text part of a checked org-mode checkbox.")

    (font-lock-add-keywords
     'org-mode
     `(("^[ \t]*\\(?:[-+*]\\|[0-9]+[).]\\)[ \t]+\\(\\(?:\\[@\\(?:start:\\)?[0-9]+\\][ \t]*\\)?\\[\\(?:X\\|\\([0-9]+\\)/\\2\\)\\][^\n]*\n\\)"
        1 'org-checkbox-done-text prepend))
     'append)
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


### Reformatting an Org buffer {#reformatting-an-org-buffer}

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
(defun afs/org-remove-link ()
    "Replace an org link by its description or if empty its address"
  (interactive)
  (if (org-in-regexp org-bracket-link-regexp 1)
      (let ((remove (list (match-beginning 0) (match-end 0)))
        (description (if (match-end 3)
                 (org-match-string-no-properties 3)
                 (org-match-string-no-properties 1))))
    (apply 'delete-region remove)
    (insert description))))
(bind-key "C-c C-M-u" 'afs/org-remove-link)
```


### Code for org-mode macros {#code-for-org-mode-macros}

Here I define functions which get used in some of my org-mode macros

The first is a support function which gets used in some of the following, to return a string (or an optional custom  string) only if  it  is a non-zero, non-whitespace string,  and `nil` otherwise.

```emacs-lisp
(defun zz/org-if-str (str &optional desc)
  (when (org-string-nw-p str)
    (or (org-string-nw-p desc) str)))
```

This function receives three arguments, and returns the org-mode code for a link to the Hammerspoon API documentation for the `link` module, optionally to a specific `function`. If `desc` is passed, it is used as the display text, otherwise `section.function` is used.

```emacs-lisp
(defun zz/org-macro-hsapi-code (module &optional func desc)
  (org-link-make-string
   (concat "https://www.hammerspoon.org/docs/"
           (concat module (zz/org-if-str func (concat "#" func))))
   (or (org-string-nw-p desc)
       (format "=%s="
               (concat module
                       (zz/org-if-str func (concat "." func)))))))
```

Split STR at spaces and wrap each element with the `~` char, separated by `+`. Zero-width spaces are inserted around the plus signs so that they get formatted correctly. Envisioned use is for formatting keybinding descriptions. There are two versions of this function: "outer" wraps each element in  `~`, the "inner" wraps the whole sequence in them.

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
(defun zz/org-macro-luadoc-code (func &optional section desc)
  (org-link-make-string
   (concat "https://www.lua.org/manual/5.3/manual.html#"
           (zz/org-if-str func section))
   (zz/org-if-str func desc)))
```

```emacs-lisp
(defun zz/org-macro-luafun-code (func &optional desc)
  (org-link-make-string
   (concat "https://www.lua.org/manual/5.3/manual.html#"
           (concat "pdf-" func))
   (zz/org-if-str (concat "=" func "()=") desc)))
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

First, load `ox-leanpub-markdown`. This is based on Juan's `ox-leanpub`, but with many changes of my own, including a rename.  You can get it from my fork at <https://github.com/zzamboni/ox-leanpub/tree/book-and-markua>.

```emacs-lisp
(use-package ox-leanpub-markdown
  :defer 1
  :ensure nil
  :after org
  :load-path "lisp/ox-leanpub")
```

```emacs-lisp
(use-package ox-leanpub-markua
  :defer 1
  :ensure nil
  :after org
  :load-path "lisp/ox-leanpub")
```

Next, load my `ox-leanpub-book` module (also available at  <https://github.com/zzamboni/ox-leanpub/tree/book-and-markua>). It defines a new export backend called `leanpub-book`, which adds three additional items in the LeanPub export section:

-   "Multifile: Whole book", which exports the whole book as one-file-per-chapter;
-   "Multifile: Subset", which exports only the chapters that should be included in `Subset.txt` (if any), according to the rules listed below. I use this together with `#+LEANPUB_WRITE_SUBSET: current` in my files to quickly export only the current chapter, to be able to quickly preview it using [LeanPub's subset-preview feature](https://leanpub.com/help/manual#subsetpreview);
-   "Multifile: Current chapter" to explicitly export only the current chapter to its own file. This also updates `Subset.txt`, so it can be used to preview the current chapter without having to set `#+LEANPUB_WRITE_SUBSET: current`.

The book files are populated as follows:

-   `Book.txt` with all chapters, except those tagged with `noexport`.
-   `Sample.txt` with all chapters tagged with `sample`.
-   `Subset.txt` with chapters depending on the value of the `#+LEANPUB_WRITE_SUBSET` file property (if set):
    -   Default or `none`: not created.
    -   `tagged`: use all chapters tagged `subset`.
    -   `all`: use the same chapters as `Book.txt`.
    -   `sample`: use same chapters as `Sample.txt`.
    -   `current`: export the current chapter (where the cursor is at the moment of the export) as the contents of `Subset.txt`.

If a heading has the `frontmatter`, `mainmatter` or `backmatter` tags, the corresponding markup is inserted in the output, before the headline. This way, you only need to tag the first chapter of the front, main, and backmatter, respectively.

Note that the `org-leanpub-book-setup-menu-markdown` function gets called in the `:config` section. This is because I am working on `ox-markua` to export Leanpub's new [Markua](https://leanpub.com/markua/read) format, and I plan for `ox-leanpub-book` to also support it.

```emacs-lisp
(use-package ox-leanpub-book
  :defer 1
  :ensure nil
  :after ox-leanpub-markdown
  :load-path "lisp/ox-leanpub"
  :config
  (progn (org-leanpub-book-setup-menu-markdown)
         (org-leanpub-book-setup-menu-markua)))
```


### Miscellaneous org functions and configuration {#miscellaneous-org-functions-and-configuration}

Utility `org-get-keyword` function (from the org-mode mailing list) to get the value of file-level properties.

```emacs-lisp
(defun org-get-keyword (key)
  (org-element-map (org-element-parse-buffer 'element) 'keyword
    (lambda (k)
      (when (string= key (org-element-property :key k))
        (org-element-property :value k)))
    nil t))
```

[org-sidebar](https://github.com/alphapapa/org-sidebar) provides a configurable sidebar  to org buffers, showing the agenda, headlines, etc.

```emacs-lisp
(use-package org-sidebar)
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

Desktop mode also includes the `desktop-clear` function, which can be used to kill all open buffers. I bind it to <kbd>Control-Meta-super-k</kbd>.

```emacs-lisp
(use-package desktop
  :defer nil
  :custom
  (desktop-restore-eager   1 "Restore the first buffer right away")
  (desktop-lazy-idle-delay 1 "Restore the other buffers 1 second later")
  (desktop-lazy-verbose  nil "Be silent about lazily opening buffers")
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

I like to highlight the current line. For this I use the built-in `hl-line`.

```emacs-lisp
(use-package hl-line
  :defer nil
  :config
  (defun zz/get-visual-line-range ()
    (let (b e)
      (save-excursion
        (beginning-of-visual-line)
        (setq b (point))
        (end-of-visual-line)
        (setq e (+ 1 (point)))
        )
      (cons b e)))
  (setq hl-line-range-function #'zz/get-visual-line-range)
  (global-hl-line-mode))
```

I also provide a custom value for `hl-line-range-function` (thanks to Eric on the [org-mode mailing list](https://lists.gnu.org/archive/html/emacs-orgmode/2019-10/msg00303.html) for the tip) which highlights only the current visual line in `visual-line-mode`, which I use for Org-mode files (see [Beautifying org-mode](#beautifying-org-mode)).

```emacs-lisp
(defun zz/get-visual-line-range ()
  (let (b e)
    (save-excursion
      (beginning-of-visual-line)
      (setq b (point))
      (end-of-visual-line)
      (setq e (+ 1 (point)))
      )
    (cons b e)))
(setq hl-line-range-function #'zz/get-visual-line-range)
```

I have also experimented with highlighting the current column. At the moment the code below is all disabled because I find it too distracting, but I'm leaving it  here for reference. I found two options to achieve this:

-   The `col-highlight` package, which highlights the column only after a defined interval has passed
-   The `crosshairs` package, which always highlights both the column and the line. It also has a "highlight crosshairs when idle" mode, but I prefer to have the current line always highlighted.

<!--listend-->

```emacs-lisp
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
  :custom
  (neo-theme (if (display-graphic-p) 'icons 'arrow))
  (neo-smart-open t)
  (projectile-switch-project-action 'neotree-projectile-action)
  :config
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
  :defer 3
  :hook
  (org-journal-mode . wc-mode))
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

(use-package swiper-helm
  :bind
  ("C-s" . swiper))
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

I find `iedit` absolutely indispensable when coding. In short: when you hit `Ctrl-:`, all occurrences of the symbol under the cursor (or the current selection) are highlighted, and any changes you make on one of them will be automatically applied to all others. It's great for renaming variables in code, but it needs to be used with care, as it has no idea of semantics, it's  a plain string replacement, so it can inadvertently modify unintended parts of the code.

```emacs-lisp
(use-package iedit
  :config
  (set-face-background 'iedit-occurrence "Magenta")
  :bind
  ("C-;" . iedit-mode))
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
  :diminish)
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

Use `emr` for supporting refactoring in Emacs LISP and some other languages.

```emacs-lisp
(use-package emr
  :config
  (bind-key "A-RET" 'emr-show-refactor-menu prog-mode-map))
```

When coding in LISP-like languages, `rainbow-delimiters` is a must-have - it marks each concentric pair of parenthesis with different colors, which makes it much easier to understand expressions and spot mistakes.

```emacs-lisp
(use-package rainbow-delimiters
  :hook
  ((prog-mode cider-repl-mode) . rainbow-delimiters-mode))
```

Another useful addition for LISP coding - `smartparens` enforces parenthesis to match, and adds a number of useful operations for manipulating parenthesized expressions. I map `M-(` to enclose the next expression as in `paredit` using a custom function. Prefix argument can be used to indicate how many expressions to enclose instead of just 1. E.g. `C-u 3 M-(` will enclose the next 3 sexps.

```emacs-lisp
(defun zz/sp-enclose-next-sexp (num)
  (interactive "p")
  (insert-parentheses (or num 1)))

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
  (smartparens-mode  . (lambda ()
                         (local-set-key (kbd "M-(")
                                        'zz/sp-enclose-next-sexp))))
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

-   [Dockerfile files](https://github.com/spotify/dockerfile-mode)

    ```emacs-lisp
    (use-package dockerfile-mode)
    ```

-   [The Dhall configuration language](https://dhall-lang.org/)

    ```emacs-lisp
    (use-package dhall-mode
      :ensure t
      :mode "\\.dhall\\'")
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
                       (sort (mapcar
                              (lambda (x)
                                (cons (random) (concat x "\n")))
                              lines)
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

<!--listend-->

```emacs-lisp
(defmacro measure-time (&rest body)
  "Measure the time it takes to evaluate BODY."
  `(let ((time (current-time)))
     ,@body
     (message "%.06f" (float-time (time-since time)))))
```

-   Trying out [Deft](https://github.com/jrblevin/deft)

    ```emacs-lisp
    (use-package deft
      :custom
      (deft-use-filename-as-title nil)
      (deft-use-filter-string-for-filename t)
      (deft-file-naming-rules '((noslash . "-")
                                (nospace . "-")
                                (case-fn . downcase)))
      (deft-org-mode-title-prefix t)
      (deft-extensions '("org" "txt" "text" "md" "markdown"))
      (deft-default-extension "org"))
    ```

-   Ability to [restart Emacs from within Emacs](https://github.com/iqbalansari/restart-emacs):

    ```emacs-lisp
    (use-package restart-emacs)
    ```

-   [Multiple cursors](https://github.com/magnars/multiple-cursors.el)

    ```emacs-lisp
    (use-package multiple-cursors
      :bind
      ("C-c m c"   . mc/edit-lines)
      ("C-c m <"   . mc/mark-next-like-this)
      ("C-c m >"   . mc/mark-previous-like-this)
      ("C-c m C-<" . mc/mark-all-like-this))
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

-   `undo-tree` visualises undo history as a tree for easy navigation (found about this from [Jamie's config](https://jamiecollinson.com/blog/my-emacs-config/#better-undo))

    ```emacs-lisp
    (use-package undo-tree
      :ensure t
      :diminish undo-tree-mode
      :config
      (global-undo-tree-mode 1))
    ```


## Cheatsheet and experiments {#cheatsheet-and-experiments}

Playground and how to do different things, not necessarily used in my Emacs config but useful sometimes.

This is how we get a global header property in org-mode

```emacs-lisp
(alist-get :tangle
           (org-babel-parse-header-arguments
            (org-entry-get-with-inheritance "header-args")))
```

Testing formatting org snippets to look like noweb-rendered output (disabled for now).

```emacs-lisp
(eval-after-load 'ob
  (customize-set-variable
   'org-entities-user
   '(("llangle" "\\llangle" t "&lang;&lang;" "<<" "<<" "«")
     ("rrangle" "\\rrangle" t "&rang;&rang;" ">>" ">>" "»")))
  (setq org-babel-exp-code-template
        (concat "\n@@latex:\\noindent@@\\llangle​//​\\rrangle\\equiv\n"
                org-babel-exp-code-template)))
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

A work-in-progress Hammerspoon shell for Emacs, posted on the Hammerspoon mailing list.

```emacs-lisp
;;===> hammerspoon-shell
;; Quick and dirty shell with interactive history search and persistence
;; Just drop into your ~/.emacs file.
;;
;; A hammerspoon buffer is any lua buffer visiting a pathname like
;;    **/*hammerspoon**/*.lua
;; Usage: M-x hammerspoon-shell, or Hyper-s in a hammerspoon buffer.
;; In any hammerspoon buffer, Hyper-c runs dofile(file) on the visited file.
;;
;; Tip: to reload a Spoon "MySpoon" without hs.reload:
;; package.loaded.MySpoon=false hs.spoons.use("MySpoon",{config={debug=true})
(add-hook 'lua-mode-hook
          (lambda ()
            (when (string-match "hammerspoon" buffer-file-name)
              (local-set-key (kbd "H-s") #'hammerspoon-shell)
              (local-set-key
               (kbd "H-c")
               (lambda ()
                 (interactive)
                 (save-buffer)
                 (let ((name buffer-file-name))
                   (unless (and (boundp 'hammerspoon-buffer)
                                (buffer-live-p hammerspoon-buffer))
                     (hammerspoon-shell))
                   (with-current-buffer hammerspoon-buffer
                     (goto-char (point-max))
                     (insert (concat "dofile(\"" name "\")"))
                     (comint-send-input))))))))

(defvar hammerspoon-buffer nil)
(defun hammerspoon-shell ()
  (interactive)
  (if (and hammerspoon-buffer (comint-check-proc hammerspoon-buffer))
      (pop-to-buffer hammerspoon-buffer)
    (setq hammerspoon-buffer (make-comint "hammerspoon"
                                          "/usr/local/bin/hs" nil "-C"))
    (let* ((process (get-buffer-process hammerspoon-buffer))
           (history-file "~/.hammerspoon/.hs-history"))
      (pop-to-buffer hammerspoon-buffer)
      (turn-on-comint-history history-file)
      (local-set-key (kbd "<down>") (lambda() (interactive)
                                      (comint-move-or-history nil)))
      (local-set-key (kbd "<up>") (lambda() (interactive)
                                    (comint-move-or-history 'up))))))

;; Comint configs and extensions
(setq comint-input-ring-size 1024
      comint-history-isearch 'dwim)
(defun comint-move-or-history (up &optional arg)
  "History if at process mark, move otherwise"
  (interactive)
  (let* ((proc (get-buffer-process (current-buffer)))
         (proc-pos (if proc (marker-position (process-mark proc))))
         (arg (or arg 1))
         (arg (if up arg (- arg))))
    (if (and proc
             (if up
                 (= (line-number-at-pos) (line-number-at-pos proc-pos))
               (= (line-number-at-pos) (line-number-at-pos (point-max)))))
        (comint-previous-input arg)
      (forward-line (- arg)))))

(defun comint-write-history-on-exit (process event)
  (comint-write-input-ring)
  (let ((buf (process-buffer process)))
    (when (buffer-live-p buf)
      (with-current-buffer buf
        (insert (format "\nProcess %s %s" process event))))))

(defun turn-on-comint-history (&optional file)
  (let ((process (get-buffer-process (current-buffer))))
    (when process
      (setq comint-input-ring-file-name
            (or file
                (format "~/.emacs.d/inferior-%s-history"
                        (process-name process))))
      (comint-read-input-ring)
      ;; Ensure input ring gets written
      (add-hook 'kill-buffer-hook 'comint-write-input-ring nil t)
      (set-process-sentinel process
                            #'comint-write-history-on-exit))))

;; Ensure all input rings get written on exit
(defun comint-write-input-ring-all-buffers ()
  (mapc (lambda (buffer)
          (with-current-buffer buffer
            (comint-write-input-ring)))
        (buffer-list)))
(add-hook 'kill-emacs-hook 'comint-write-input-ring-all-buffers)
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
