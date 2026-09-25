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
4. stores it under `static/img/generated/<slug>.webp`,
5. updates the feature-image metadata,
6. creates a branch and pull request against the branch from which the workflow
   was launched.

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
OPENAI_API_KEY=... python scripts/generate-feature-image.py generate path/to/post.md
```

Add `--extra-prompt "..." ` for art direction. Existing non-default feature
images are protected unless `--force` is supplied.
