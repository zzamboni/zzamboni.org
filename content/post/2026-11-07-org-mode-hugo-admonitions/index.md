+++
title = "Bringing modern admonitions to Org mode and Hugo"
author = ["Diego Zamboni"]
summary = "How I map Org special blocks to Blowfish admonitions, keep old tip and warning blocks working, and choose icons or colors without duplicating the theme's renderer."
date = 2026-11-07T00:00:00+01:00
tags = ["blogging", "orgmode", "hugo", "blowfish", "howto"]
draft = true
creator = "Emacs (Org mode + ox-hugo)"
toc = false
+++

I have used `tip`, `note`, and `warning` blocks in my Org-authored articles for years. They are useful little interruptions: a shortcut worth knowing, some background, or a warning before running a command.

After moving to [Blowfish](https://blowfish.page/), I wanted those blocks to use the theme's modern admonition styling, including its icons and light/dark palettes. I also wanted old articles to benefit without rewriting their source. The solution turned out to be a small adapter between `ox-hugo` and the theme.


## Start with the Org block {#start-with-the-org-block}

The authoring syntax is ordinary Org:

```org
#+begin_tip
Use =mise run serve-drafts= to preview unfinished articles.
#+end_tip
```

I register the block names as paired shortcodes in the Org file, alongside the other shortcodes I already use:

```org
#+hugo_paired_shortcodes: tip warning note gallery feature-grid mermaid alert admonition
```

That registration matters. It tells [ox-hugo](https://ox-hugo.scripter.co/doc/shortcodes/) to export a matching Hugo shortcode call, with an opening and closing tag, instead of treating the special block as a generic HTML container. The block's contents still go through Org export, so I can use links, lists, and source blocks inside it.


## Let Blowfish do the rendering {#let-blowfish-do-the-rendering}

Blowfish already renders Markdown alerts such as a blockquote beginning with `[!TIP]`. I reuse that path rather than maintaining another set of callout HTML and CSS.

My `tip`, `note`, and `warning` shortcode files all delegate to the same partial. Hugo supplies the invoked shortcode's name, and the partial turns its body into a Markdown blockquote:

```go-html-template
{{- /* Keep legacy shortcode calls, but let Blowfish's blockquote hook render them. */ -}}
{{- $body := strings.Trim .Inner "\r\n" -}}
{{- $markdown := printf "> [!%s]\n%s" (strings.ToUpper .Name) (replaceRE "(?m)^" "> " $body) -}}
{{- with .Icon -}}
  {{- $markdown = printf "%s\n{icon=%q}" $markdown . -}}
{{- end -}}
{{- .Page.RenderString (dict "display" "block") $markdown -}}
```

Every line gets a quote prefix, including blank lines, so multiple paragraphs and code blocks stay inside the callout. `RenderString` then sends the constructed Markdown through the page's render hooks. Blowfish's blockquote hook supplies the title, icon, palette, and final markup.

The optional icon is added as a block attribute understood by the theme. The important dependency is that render hook: this adapter is designed for Blowfish's admonition support, and I track it with my other theme overrides.


## One block for more types {#one-block-for-more-types}

The three original block names remain convenient, but I do not want a new shortcode file for every possible callout type. A generic `admonition` shortcode accepts a `type` parameter and passes it to the same partial:

```org
#+attr_shortcode: :type important :icon star
#+begin_admonition
Keep the Org source and its Markdown export together.
#+end_admonition
```

The generic block defaults to `note`. Other types come from Blowfish's supported admonitions, including `caution`, `question`, and `example`. Named arguments use Org's `:name value` syntax in `#+attr_shortcode`; `#+attr_html` would target a different part of the export.

For an ordinary tip, I can override just its icon:

```org
#+attr_shortcode: :icon star
#+begin_tip
A useful trick deserves a memorable icon.
#+end_tip
```


## Colors have two different paths {#colors-have-two-different-paths}

Admonition colors follow the selected type. For a site-wide change I can override variables such as `--adm-tip-bg` in my own CSS, with separate light and dark values.

For one individually styled box, I use Blowfish's separate `alert` shortcode:

```org
#+attr_shortcode: :icon fire :cardColor #e63946 :iconColor #ffffff :textColor #ffffff
#+begin_alert
Review this operation before continuing.
#+end_alert
```

The admonition adapters only forward the icon override; they do not forward those color parameters. The alert also has a different layout, without an automatic admonition title. Explicit colors need a contrast check in both appearances.


## Old markup, new presentation {#old-markup-new-presentation}

The nicest part is that existing shortcode calls keep working. Once the adapters are in place, rebuilding the site gives old articles the new rendering. I can improve their presentation while leaving their content alone.

The [full configuration notes](https://github.com/zzamboni/zzamboni.org/blob/main/docs/callout-blocks.md) cover the aliases, supported parameters, and palette overrides. For everyday writing, all I need to remember is the block name and, occasionally, a line of attributes.
