# AI feature image generation

Feature images can be generated semi-automatically for Pages CMS, ox-hugo, and
legacy Markdown posts.

## GitHub Actions

Run **Generate feature image** from the Actions tab and provide the path to the
rendered Hugo post, for example:

```
content/post/reviving-an-old-mac-with-linux-part-1/index.md
```

or:

```
content-pagescms/2026-09-21-new-posting-workflow-pagescms.md
```

The workflow:

1. reads the rendered post as common input,
2. asks a text model for a visual brief,
3. generates a landscape image,
4. stores it under `assets/img/generated/<slug>.webp`,
5. updates the feature-image metadata,
6. creates a branch and pull request against the branch from which the workflow
   was launched.

In Pages CMS, use **Org posts (image actions)** to select an export under
`content/post/`. Its fields are read-only; edit post content in
`content-org/zzamboni.org`. The workflow checks for a matching ox-hugo entry
before asking the image models to run.

For ox-hugo posts, the script also updates the matching property drawer in
`content-org/zzamboni.org` so that a later export does not overwrite the
generated feature image.

The PR is deliberately not auto-merged. Review the Netlify deploy preview and
merge only if the image works well with the site.

The workflow uses the existing `OPENAI_API_KEY` repository secret. Optional
environment variables supported by the script are:

- `FEATURE_IMAGE_TEXT_MODEL` (default: `gpt-5-mini`)
- `FEATURE_IMAGE_MODEL` (default: `gpt-image-1`)
- `FEATURE_IMAGE_SIZE` (default: `1536x1024`)
- `FEATURE_IMAGE_QUALITY` (default: `medium`)

## Choosing a style

The workflow's **Image style** dropdown and the Pages CMS **Generate image** action
both offer these styles:

- **Photographic editorial image** (default)
- **Analog film photography**
- **Architectural photography**
- **Macro photography**
- **Printmaking / linocut**
- **Editorial illustration**

The selected style guides both the visual brief and image generation. Additional
artistic direction supplements the chosen style. Older action payloads that omit
the style use photographic editorial images. Generated images still require PR
review before publication.

Locally, select a style with:

```sh
python scripts/generate-feature-image.py generate path/to/post.md --style "Analog film photography"
```

## Finding older posts to improve

Locally:

```sh
pip install openai pillow pyyaml
python scripts/generate-feature-image.py candidates
```

This lists posts with no explicit feature image or with the default tram image.
Use `--limit N` to inspect a smaller batch.

To generate an image locally:

```sh
set-env OPENAI_API_KEY ...
python scripts/generate-feature-image.py generate path/to/post.md
```

Add `--extra-prompt "..." ` for art direction. Existing non-default feature
images are protected unless `--force` is supplied.
