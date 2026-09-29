# Photo posts from iOS

The staging deployment accepts `POST /api/photoblog`. It creates a draft Hugo
page bundle in `content/post/`, with the first image named `feature.jpg` (or
`feature.png` / `feature.webp`) for Blowfish's article list. The body uses
Blowfish's `gallery` and `figure` shortcodes. The `photos` tag makes the post
appear in the Photos menu. No Org source is involved for these mobile posts.

The function reuses `LINKBLOG_SECRET` and `LINKBLOG_GITHUB_TOKEN` from the
linkblog function. Optional `PHOTOBLOG_SECRET` and `PHOTOBLOG_GITHUB_TOKEN`
override them. Set `PHOTOBLOG_BRANCH=staging` in the staging Netlify site's
environment variables, with the Functions scope, then redeploy. If you later
promote this function to the production and draft sites, set
`PHOTOBLOG_BRANCH=main` there. Netlify's built-in `BRANCH` is available to
builds but not to deployed Functions, so an unset branch is an error instead
of defaulting to `main`. Use the staging site's URL while experimenting.

## Build the shortcut

1. Create a new shortcut, enable **Show in Share Sheet**, and accept **Images**.
   In Photos, select one or several pictures and share them to the shortcut.
2. Add **Ask for Input** (Text) for a title; leave it blank to use the current
   Zürich date. Add another optional Text prompt for commentary.
3. **Repeat with Each** item from **Shortcut Input**. Within the loop, use
   **Resize Image** (for example, width 1600 px), **Convert Image** to JPEG,
   then **Base64 Encode**. Add each encoded string to a variable named
   `EncodedPhotos`. If the converted photos are too large, lower the JPEG
   quality or size. The function accepts 1–6 images, at most 2.5 MB per
   image and 3 MB total after decoding.
4. Add a **Dictionary** with `title` (Text), `commentary` (Text), `date`
   (Text: current date formatted ISO 8601, with timezone), and `photos`
   (the `EncodedPhotos` list). You can omit `date` and `tags` entirely;
   the server uses the current Zürich time and adds the `photos` tag.
5. Add **Get Contents of URL** for
   `https://YOUR-STAGING-SITE.netlify.app/api/photoblog`. Select `POST`,
   add the header `Authorization: Bearer YOUR_LINKBLOG_SECRET` (one space
   after `Bearer`), set Request Body to **JSON**, and use the dictionary's
   values for the corresponding keys. Store the secret only in your own
   shortcut. A JSON response contains `editUrl` for the new draft.
6. Use **Get Dictionary Value** for `editUrl` from the response, then **Open
   URLs** if you want to inspect the Markdown in GitHub. Review the staging
   draft before publishing it by changing `draft = true` to `false`.

The staging site currently does not build drafts. To see an upload there,
include `draft: false` in the shortcut's JSON dictionary while testing, or
enable draft builds on that staging Netlify site. Omit `draft` for production
uploads so they remain unpublished until you review them. Switch the URL to
the production site's `/api/photoblog` only when you are ready to write to
`main`; do not merge test photo posts from `staging` into `main`.

The request shape is:

```json
{
  "title": "A walk by the lake",
  "commentary": "Optional brief note.",
  "date": "2026-09-29T14:00:00+02:00",
  "photos": ["<base64 JPEG>", "<base64 JPEG>"],
  "draft": false,
  "tags": ["zurich"]
}
```

JPEG, PNG and WebP are supported. iPhone HEIC photos should be converted to
JPEG in the shortcut before Base64 encoding. Each invocation creates one
draft post with all selected photos. Image bytes are committed with the
Markdown in a single GitHub commit; no half-written bundles are exposed.
