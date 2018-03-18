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
