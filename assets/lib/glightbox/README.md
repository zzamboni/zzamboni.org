# GLightbox 3.3.1

Vendored unchanged from https://github.com/biati-digital/glightbox/tree/v3.3.1:

- dist/js/glightbox.min.js
- dist/css/glightbox.min.css
- LICENSE.md (MIT)

These assets load only on pages with a photos frontmatter field, through Hugo Pipes
with fingerprinting. The site adapter is assets/js/photo-lightbox.js; the gallery
layout remains Blowfish's. To update, replace both distribution files together and
retain the upstream license.

Preview checks: open each thumbnail, next/previous and wraparound, keyboard arrows,
Escape, Tab/Shift-Tab and focus restoration, single-photo posts, iPhone swiping and
pinch zoom, desktop zoom/drag, reduced motion, and ordinary links without JavaScript.
