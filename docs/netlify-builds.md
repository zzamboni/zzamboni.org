# Netlify build filtering

`netlify.toml` runs `node ./scripts/netlify-ignore.mjs` before dependency
installation. It requires only Node's standard library and Git.

The script skips a build only when every changed path is one of:

- Root `README.md`, `AGENTS.md`, or `.pages.yml`.
- Files under `docs/` or `scripts/tests/`.
- `.org` authoring files under `content-org/` (Hugo builds their exports).

Images under `content-org/`, exported content, all publishing directories,
functions, dependencies, theme pointers, configuration, workflows, scripts,
and unknown paths continue to build. Keep this list aligned with template
dependencies: if Hugo starts reading a currently excluded file, remove the
exclusion. Do not skip all bot commits; generated summaries/images affect output.

Comparisons span `CACHED_COMMIT_REF` to `COMMIT_REF`, not just the last commit.
Renames check both paths. Missing refs/history, Git errors, and identical refs
build conservatively. This is particularly relevant to shallow checkouts.
The check does not fetch history or change the repository.

Set `NETLIFY_FORCE_BUILD=true` in the Netlify build environment to bypass the
filter. Netlify build hooks bypass ignore checks independently. Exit 0 means
skip and exit 1 means build; an exit 1 in a local test is not a script failure.

Run `node --test scripts/tests/netlify-ignore.test.mjs` to test the policy.
No live build settings are changed by adding this file. The policy takes effect
when the configuration reaches each deployed branch; verify the printed
`[netlify-ignore]` decision in the next build log.
