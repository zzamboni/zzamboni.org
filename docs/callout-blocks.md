# Callout blocks in Org mode

Use these blocks in `content-org/zzamboni.org`, then export the article with
ox-hugo as usual.

## Choosing a block

| Org block | Use for | Rendering | Default icon | Colors |
| --- | --- | --- | --- | --- |
| `tip` | Suggestions and useful shortcuts | Blowfish Tip admonition | `lightbulb` | Green palette, with light/dark variants |
| `note` | Background information and clarifications | Blowfish Note admonition | `circle-info` | Blue palette, with light/dark variants |
| `warning` | Risks and things requiring care | Blowfish Warning admonition | `triangle-exclamation` | Orange palette, with light/dark variants |
| `admonition` | Any supported admonition type | Blowfish admonition selected by `type` | From the selected type | From the selected type; defaults to Note |
| `alert` | A message with individually chosen styling | Blowfish alert shortcode | `triangle-exclamation` | Theme colors by default; optional explicit overrides |

The first three include an automatic title (Tip, Note, or Warning). The
`alert` shortcode is a different layout: it shows an icon beside the content,
without adding an admonition title.

## Basic examples

```org
#+begin_tip
Use =mise run serve-drafts= to preview unpublished articles locally.
#+end_tip

#+begin_note
The Org file is the source of truth for this article.
Edit it and export again to update the Markdown.
#+end_note

#+begin_warning
Review the changes before merging into =main=.
A push to that branch can trigger a production build.
#+end_warning

#+begin_alert
This is a general message using the theme's default colors.
#+end_alert
```

Write the contents as normal Org text. Emphasis, links, paragraphs, lists,
and source blocks are exported by ox-hugo before Hugo renders the callout.

```org
#+begin_tip
Before publishing:

- Review the preview.
- Check links and images.

See [[https://blowfish.page/docs/shortcodes/][the Blowfish shortcode documentation]] for more options.
#+end_tip
```

## Generic admonitions

Use `admonition` to select a type without adding another named shortcode:

```org
#+attr_shortcode: :type important :icon star
#+begin_admonition
Keep this information in mind.
#+end_admonition

#+attr_shortcode: :type caution
#+begin_admonition
This operation can remove data.
#+end_admonition

#+begin_admonition
Without a type, this renders as a Note.
#+end_admonition
```

The `type` parameter is case-insensitive. Blowfish supports the GitHub types
`note`, `tip`, `important`, `warning`, and `caution`, plus Obsidian types
such as `info`, `success`, `question`, `danger`, `bug`, `example`, and `quote`.
Use a supported type so the theme supplies its palette and icon.

An optional `icon` overrides the type's default icon. Colors follow the
selected type; use `alert` for individual color overrides.

The existing `tip`, `note`, and `warning` blocks remain convenient aliases.
A new named Org block would need a matching shortcode file and registration,
but new types used through `admonition` need neither.

## Change an individual icon

Put `#+attr_shortcode` immediately above the block. Named arguments use Org
property syntax: `:icon star`, rather than `icon="star"`.

```org
#+attr_shortcode: :icon star
#+begin_tip
A particularly useful tip!
#+end_tip

#+attr_shortcode: :icon circle-info
#+begin_note
Some additional context.
#+end_note

#+attr_shortcode: :icon fire
#+begin_warning
Be careful with this operation.
#+end_warning
```

Use an icon name from `themes/blowfish/assets/icons/`, without `.svg`.
Custom SVG icons can be added under the site's `assets/icons/` directory.
The same `:icon` parameter works on `alert`.

For example, ox-hugo turns the first example into:

```go-html-template
{{< tip icon="star" >}}
A particularly useful tip!
{{< /tip >}}
```

## Choose colors for one box

The `tip`, `note`, `warning`, and generic `admonition` adapters accept an optional `icon`.
They do **not** forward `cardColor`, `iconColor`, or `textColor`.
Their colors are determined by the admonition type.

Use `alert` when one box needs explicit colors:

```org
#+attr_shortcode: :icon fire :cardColor #e63946 :iconColor #ffffff :textColor #ffffff
#+begin_alert
*Attention:* this operation needs extra care.
#+end_alert
```

| Parameter | Meaning |
| --- | --- |
| `icon` | Icon name, without `.svg` |
| `cardColor` | Box background color |
| `iconColor` | Icon color |
| `textColor` | Content text color |

Colors can be CSS color names or hexadecimal values. Omit color parameters
to retain Blowfish's defaults. Explicit colors remain the same in light and
dark mode, so check contrast in both.

## Change the palette for all blocks of a type

For a site-wide change, edit `assets/css/custom.css`. Blowfish provides
CSS variables for each admonition type. For example, this changes every
Tip admonition, including those produced by the `tip` shortcode:

```css
:root {
  --adm-tip-border: #7c3aed;
  --adm-tip-bg: #f5f3ff;
  --adm-tip-text: #4c1d95;
}

html.dark {
  --adm-tip-border: #a78bfa;
  --adm-tip-bg: #2e1065;
  --adm-tip-text: #ede9fe;
}
```

Replace `tip` with `note` or `warning` to customize those palettes.
These variables do not style the separate `alert` shortcode.
Keep these overrides in the site's CSS rather than editing theme files.

## Export setup

The Org source currently registers all five blocks, along with other
paired shortcodes:

```org
#+hugo_paired_shortcodes: tip warning note gallery feature-grid mermaid alert admonition
```

When adding blocks to another Org file, include their names in that file's
`#+hugo_paired_shortcodes` declaration. Preserve any existing shortcode names.

Without registration, an Org special block may export as an HTML block
instead of calling the Hugo shortcode. Use `#+attr_shortcode`, rather than
`#+attr_html`, for the shortcode parameters shown above.

## How the adapters work

The three templates in `layouts/shortcodes/{tip,note,warning}.html` have
identical contents. Hugo sets `.Name` from the invoked shortcode's name,
so each passes a different value to
`layouts/partials/shortcode-admonition.html`.

The generic `layouts/shortcodes/admonition.html` passes its `type` parameter\n(defaulting to `note`) as `Name` to the same partial.\n\nThe partial:\n
1. Builds a Markdown alert marker from the uppercase name, such as `[!TIP]`,\n   `[!NOTE]`, `[!WARNING]`, or `[!IMPORTANT]`.
2. Prefixes every content line with `> ` to keep the entire body inside
   the blockquote, including blank lines.
3. Adds `{icon="…"}` when a custom icon was supplied.
4. Calls `.Page.RenderString` in block mode, letting Blowfish's blockquote
   render hook produce the final HTML.

Existing articles keep their shortcode calls while using the theme's
admonition rendering. The dependency on the theme hook is recorded in
`scripts/theme-overrides.toml`.

The `alert` block goes directly to Blowfish's existing
`layouts/shortcodes/alert.html`; it does not use our adapter.

## Preview locally

After exporting the Org article, run from the repository root:

```elvish
mise run serve-drafts
```

Check the boxes in both light and dark mode, particularly when using
explicit alert colors.

## References

- [ox-hugo: shortcodes and named arguments](https://ox-hugo.scripter.co/doc/shortcodes/)
- [Blowfish: admonitions](https://blowfish.page/docs/shortcodes/#admonition)
- [Blowfish: alert shortcode](https://blowfish.page/docs/shortcodes/#alert)
- [Pinned theme admonition CSS](https://github.com/nunocoracao/blowfish/blob/ebe683e9c2668972b71bc011e61e0004ff8e7689/assets/css/components/admonition.css)
