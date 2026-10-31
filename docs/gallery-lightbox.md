# Gallery lightbox layout and regression checks

Both the `gallery` shortcode and photoblog galleries use the shared
`assets/js/photo-lightbox.js` and `assets/css/photo-lightbox.css`. The assets
are loaded conditionally by `layouts/partials/extend-head-uncached.html`.
Keep gallery images marked `nozoom` in rendered HTML so Blowfish's regular
image zoom does not attach before GLightbox initializes.

## Images linking to pages

The local `figure` shortcode accepts ox-hugo's `link` parameter as an alias
for Blowfish's `href` (`href` wins if both are present). This keeps Org attachment
paths automatic:

```org
#+ATTR_HTML: :link https://example.org/ :class nozoom
[[attachment:post-link.png]]
```

Keep linked images outside explicit galleries, which intentionally open images
in GLightbox. The `nozoom` class prevents Blowfish's regular zoom from competing
with the link. This override otherwise follows the theme's figure shortcode;
it is detected automatically by the theme-update override review.

## Captions

The shared initializer passes each image's rendered `figcaption` to GLightbox's
native bottom description panel, preserving formatting and links. Missing or
whitespace-only captions produce no panel; image alt text remains an accessible
description and is not used as a caption fallback. Photoblog galleries currently
have no per-image captions, so their appearance is unchanged.

Captioned slides move the image counter to the top to avoid covering the panel.
Tab navigation includes links in the active caption, and mobile captions display
in full rather than using GLightbox's truncated "See more" text. The native mobile
panel supports scrolling for long captions. Local CSS gives caption text explicit
contrast instead of inheriting the site's light/dark text color on a white panel.

Run `node --test scripts/tests/photo-lightbox.test.mjs` for caption mapping tests.
Browser checks should also cover formatted/link captions, captioned-to-uncaptioned
navigation, keyboard focus, counter placement and desktop/mobile readability.

## Why the scroll-lock overrides are necessary

Blowfish centers its max-width body using `m-auto`. GLightbox 3.3.1 injects
a `.gscrollbar-fixer` right margin to compensate for a hidden scrollbar.
Overriding that margin with **zero** also breaks centering: the left margin
remains automatic, moving the entire body to the right.

Measurements on the local draft article, with a 1600px viewport and an 8px
scrollbar, confirmed this on 2026-10-27 (Blowfish 3.9.0 / Hugo 0.167.0):

| Element | Closed x | Open with old override | Open with fix |
| --- | ---: | ---: | ---: |
| Body | 156 | 312 | 156 |
| Article | 284 | 440 | 284 |
| Sticky ToC | 1080 | 1236 | 1080 |

The CSS now keeps the body's right margin automatic, reserves the root
scrollbar gutter, and locks overflow only on `html`. Body overflow stays
visible: making the body a scroll container changes the sticky ToC's
scrolling ancestor. Leaving both elements unlocked avoids that problem but
allows wheel/key scrolling behind the modal, so it is not sufficient.

The scrollbar thumb disappears during the lock, but its space remains;
document rectangles and scroll position stay unchanged. `clientWidth` alone
is not a reliable layout-shift check: Chromium reports 1600 while locked
versus 1592 before, although the root bounding rectangle remains 1592 wide.
See the [CSS scrollbar-gutter specification](https://www.w3.org/TR/css-overflow-3/#scrollbar-gutter-property).
No vendored library changes or JavaScript lifecycle workarounds are needed.

## Local verification

Run `mise run serve-drafts`, then check:

- `/post/my-blogging-setup-in-2026-more-ways-to-write-reducing-friction/`
  for shortcode galleries with a sticky ToC.
- `/post/2026-09-30-eclipse-photos-fac55636/` for a multi-photo gallery
  without a ToC.
- `/post/2026-10-06-a-perfect-spiderweb-1d814727/` for single-photo controls.

At wide desktop, laptop and mobile widths, compare `getBoundingClientRect()`
for `html`, `body`, `article`, `.article-content` and `.toc`, plus `scrollY`,
before, during and after opening. Sample animation frames, not just settled
states. Check navigation/counters, wheel/PageDown background locking, touch
swipes, Tab trapping, Escape, close-button dismissal and restored focus.
Check outside-click dismissal on desktop; GLightbox deliberately disables it
on mobile. Also verify ordinary non-gallery image zoom still opens alone.

Local Chromium automation covered desktop (1600/1280px), mobile emulation
(390px), reduced motion, multi-photo and single-photo galleries. Real-device
Safari/Firefox behavior and the deployed staging site still need a manual
check. Browser emulation is not a substitute for those checks.
