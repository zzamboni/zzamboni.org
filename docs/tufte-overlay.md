# Tufte overlay experiment

Inspired by https://github.com/loikein/hugo-tufte and its exampleSite/content/posts/tufte-css.md and tufte-features.md examples. The implementation uses original CSS and templates, with locally available Palatino/Georgia fonts.

Theme precedence is tufte-overlay, then Blowfish. The existing head hook loads the overlay stylesheet. Existing note and tip shortcodes become margin notes while the overlay is active. Warnings and other admonitions retain Blowfish rendering.

The draft demonstration is at /tufte-demo/ with mise run serve-drafts. It is an experimental fixture, authored directly in Markdown.

Supported paired shortcodes are sidenote, marginnote, newthought, epigraph (optional author parameter), and wide. Notes are block-level and should be placed between paragraphs. They remain visible inline on narrow screens. Numbered notes use CSS counters. On wide screens the table of contents moves above the article to reserve the right margin for notes.

In Org, existing begin_note and begin_tip blocks work directly. Other shortcodes can be used inside begin_export hugo blocks. Keep notes brief. Native Markdown alerts are still handled by Blowfish.

Possible follow-ups include ET Book font bundling with its license, inline note references with accessible disclosure controls, and figures with captions in the margin.
