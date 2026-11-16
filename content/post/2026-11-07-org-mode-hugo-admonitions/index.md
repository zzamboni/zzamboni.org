+++
title = "Bringing modern admonitions to Org mode and Hugo"
author = ["Diego Zamboni"]
summary = "How I map Org special blocks to Blowfish admonitions for a consistent look and feel across old and new posts."
date = 2026-11-07T00:00:00-06:00
tags = ["blogging", "orgmode", "hugo", "blowfish", "howto"]
draft = true
creator = "Emacs (Org mode + ox-hugo)"
+++

I have used `tip`, `note`, and `warning` blocks in my Org-authored articles for years. I find them useful to provide additional information: a shortcut worth knowing, some background, or a warning before running a potentially destructive command.

Some time ago I had created custom Hugo shortcodes for these blocks. `ox-hugo` allows seamless conversion from Org blocks to Hugo shortcodes by declaring them as follows near the top of my Org file, together with other shortcodes I use:

```org
#+hugo_paired_shortcodes: tip warning note alert admonition gallery feature-grid mermaid
```

Afterwards, a `#+begin_tip` / `#+end_tip` block in my Org file will be automatically exported as `{{</* tip */>}}` / `{{</* /tip */>}}` in Hugo markup to invoke the corresponding shortcodes; similarly for the others.

After moving to [Blowfish](https://blowfish.page/), I wanted to keep using these blocks, but to use the theme's modern [admonition styling](https://blowfish.page/docs/shortcodes/#admonition), including its icons and light/dark palettes. The solution was a small adapter between `ox-hugo` and the theme.


## Org block structure {#org-block-structure}

The authoring syntax is ordinary Org:

```org
#+begin_tip
Use =mise run serve-drafts= to preview unfinished articles.
#+end_tip
```

Which gets rendered as follows:

{{< tip >}}
Use `mise run serve-drafts` to preview unfinished articles.
{{< /tip >}}


## Reusing Blowfish-style rendering from Org {#reusing-blowfish-style-rendering-from-org}

Blowfish supports rendering Github-style Markdown alerts such as a blockquote beginning with `[!TIP]` (see [Admonitions](https://blowfish.page/docs/shortcodes/#admonition) for the full list of supported styles). We simply reuse this capability by exporting the blocks in the appropriate format.

My new `tip`, `note`, and `warning` shortcodes are identical, they all accept `icon` and `title` parameters and delegate to the same [shortcode-admonition](https://github.com/zzamboni/zzamboni.org/blob/experiment/commonplace-hugo/layouts/partials/shortcode-admonition.html) partial:

```go-html-template
{{- partial "shortcode-admonition.html" (dict "Inner" .Inner "Name" .Name "Page" .Page "Icon" (.Get "icon") "Title" (.Get "title")) -}}
```

Hugo supplies the invoked shortcode's name in `.Name`, so the files can be identical. This is the code of the `shortcode-admonition` partial, which turns its body into a Markdown blockquote:

```go-html-template
{{- /* Keep legacy shortcode calls, but let Blowfish's blockquote hook render them. */ -}}
{{- $body := strings.Trim .Inner "\r\n" -}}
{{- $title := strings.TrimSpace (.Title | default "") -}}
{{- $alert := printf "[!%s]" (strings.ToUpper .Name) -}}
{{- with $title -}}
  {{- $alert = printf "%s %s" $alert . -}}
{{- end -}}
{{- $markdown := printf "> %s\n%s" $alert (replaceRE "(?m)^" "> " $body) -}}
{{- with .Icon -}}
  {{- $markdown = printf "%s\n{icon=%q}" $markdown . -}}
{{- end -}}
{{- .Page.RenderString (dict "display" "block") $markdown -}}
```

Every line gets a quote prefix, including blank lines, so multiple paragraphs and code blocks stay inside the callout. `RenderString` then sends the constructed Markdown through the page's render hooks. Blowfish renders the title, icon, palette, and final markup.


## One block for more types {#one-block-for-more-types}

The three custom block names remain convenient, but I don't necessarily want a new shortcode file for every possible callout type. A generic `admonition` shortcode accepts a `type` parameter and passes it to the same partial:

```org
#+attr_shortcode: :type important :icon star
#+begin_admonition
Keep the Org source and its Markdown export together.
#+end_admonition
```

Which gets rendered as follows:

{{< admonition type="important" icon="github" >}}
Keep the Org source and its Markdown export together.
{{< /admonition >}}

The generic block defaults to `note`. Other types come from Blowfish's supported admonitions, including `caution`, `question`, and `example`. Named arguments use Org's `:name value` syntax in `#+attr_shortcode`.

The dedicated shortcodes hard-code the block type, but still allow overriding the icon with `#+attr_shortcode`:

```org
#+attr_shortcode: :icon sun
#+begin_tip
A useful trick deserves a memorable icon.
#+end_tip
```

{{< tip icon="sun" >}}
A useful trick deserves a memorable icon.
{{< /tip >}}


## Admonition colors {#admonition-colors}

Admonition colors follow the selected type. It is possible to override them site-wide, see [the Blowfish documentation](https://github.com/nunocoracao/blowfish/blob/main/layouts/_default/_markup/render-blockquote.html).

However, for individually styled boxes, I use Blowfish's separate [alert shortcode](https://blowfish.page/docs/shortcodes/#alert):

```org
#+attr_shortcode: :icon fire :cardColor #e63946 :iconColor #ffffff :textColor #ffffff
#+begin_alert
Review this operation before continuing.
#+end_alert
```

{{< alert icon="fire" cardColor="#e63946" iconColor="#ffffff" textColor="#ffffff" >}}
Review this operation before continuing.
{{< /alert >}}


## Old markup, new presentation {#old-markup-new-presentation}

The nicest part is that existing shortcode calls keep working. Once the adapters are in place, rebuilding the site gives all old articles the new rendering. I can improve their presentation while leaving their content alone.

You can find the [full configuration notes](https://github.com/zzamboni/zzamboni.org/blob/main/docs/callout-blocks.md) in my Github repo with more details. For everyday writing, all I need to remember is the block name and, occasionally, a line of attributes.

{{< admonition title="Using it yourself" type="info" >}}
If you want to use this feature in your own Org + ox-hugo website, you need to copy the following files from my repo and store them in your own:

-   [layouts/partials/shortcode-admonition.html](https://github.com/zzamboni/zzamboni.org/blob/experiment/commonplace-hugo/layouts/partials/shortcode-admonition.html)
-   [layouts/shortcodes/tip.html](https://github.com/zzamboni/zzamboni.org/blob/experiment/commonplace-hugo/layouts/shortcodes/tip.html) (same for [note.html](https://github.com/zzamboni/zzamboni.org/blob/experiment/commonplace-hugo/layouts/shortcodes/note.html) and [warning.html](https://github.com/zzamboni/zzamboni.org/blob/experiment/commonplace-hugo/layouts/shortcodes/warning.html), and you can copy the same file to create custom shortcodes for other supported admonition types)
-   [layouts/shortcodes/admonition.html](https://github.com/zzamboni/zzamboni.org/blob/experiment/commonplace-hugo/layouts/shortcodes/admonition.html)

Don't forget to declare the appropriate blocks with `#+hugo_paired_shortcodes:` in your Org file!
{{< /admonition >}}
