# Netlify build filtering

## Hugo resource caching

`netlify.toml` enables `netlify-plugin-hugo-cache-resources` for all deploy
contexts, including production, drafts, and staging. The package is pinned in
`package.json` under `dependencies` because `NODE_ENV=production` skips
devDependencies during Netlify installation. It persists Hugo's generated
`resources/` directory; it does not change browser or CDN caching.

After this configuration reaches the deployed branch, remove the redundant
UI installation from the draft project (and any other project where it was
enabled manually). File configuration takes precedence while both exist.
Verify the next build loads the plugin from `netlify.toml` and restores/saves
resources. A project's first cache-populating build may not be faster; do not
clear its cache when checking subsequent builds.

The draft-site benchmark measured median Hugo time falling from 12.9s to 3.9s
and median total processing from 39.3s to 31.4s across three runs per phase.
These were unchanged-content builds; new images still require processing.

## Build filtering

`netlify.toml` runs `node ./scripts/netlify-ignore.mjs` before dependency
installation. It requires only Node's standard library and Git.

By default, the script skips a build only when every changed path is one of:

- Root `README.md`, `AGENTS.md`, or `.pages.yml`.
- Files under `docs/`, `scripts/`, or `.github/workflows/`.
- `.org` authoring files under `content-org/` (Hugo builds their exports).

Images under `content-org/`, exported content, all publishing directories,
functions, dependencies, theme pointers, site configuration,
and unknown paths continue to build. Keep this list aligned with template
dependencies: if Hugo starts reading a currently excluded file, remove the
exclusion. Do not skip all bot commits; generated summaries/images affect output.

Workflow definitions do not affect the Netlify build directly. Content or assets
committed by those workflows still trigger builds normally.

`scripts/` currently contains authoring, maintenance, and test tooling, not
site-build or function-runtime dependencies. Its generated content and assets
still trigger builds. The ignore script itself runs from the checked-out commit,
so changes to its policy take effect without publishing a new site deploy.
Revisit this exclusion if the build command or deployed functions start using
other scripts from this directory.

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

## On-demand draft builds

Set `NETLIFY_ON_DEMAND=true` only on the draft project's build environment,
alongside its existing `BUILD_DRAFTS=true`. This skips all builds that run the
ignore check, even with missing Git history or site changes. Production is
unaffected when the variable is unset. Only the exact value `true` enables it.

Leave Netlify builds Active and create a build hook targeting `main` on the
draft project. Invoke that hook to refresh drafts; Netlify build hooks bypass
the ignore check. Do not use Stopped builds, which also disables hooks.
Ordinary UI-triggered builds are not the supported bypass for this policy.

`NETLIFY_FORCE_BUILD=true` takes precedence over on-demand mode. Unset it after
use to restore on-demand behavior. Keep hook URLs private and outside Git.
This feature becomes effective once the script change reaches the branch the
draft project builds; setting the environment variable alone is insufficient.

### Trigger from Pages CMS or GitHub

The repository-level **Build draft site** action in Pages CMS dispatches
`.github/workflows/build-draft-site.yml` on `main`. It always rebuilds the latest
saved content on `main`, including all drafts, regardless of the branch open in
the CMS. Save edits first; unsaved edits and staging-only changes are not included.

One-time setup:

1. On the **draft** Netlify project, create or reuse a build hook targeting `main`.
2. In GitHub repository Settings > Secrets and variables > Actions, add the
   repository secret `NETLIFY_DRAFT_BUILD_HOOK` with that hook's URL. Do not use
   a production-project hook or commit the URL.
3. Promote the workflow and CMS configuration to `main` before using the button.
   Keep the draft project's builds Active and `NETLIFY_ON_DEMAND=true`.

Alternatively, open GitHub Actions > Build draft site > Run workflow, select
`main`, and leave `payload` blank. Other workflow branches are rejected.
The CMS payload is accepted for compatibility but does not control the hook or
target branch. The workflow needs no checkout or GitHub token permissions.

A successful action means Netlify accepted the request, not that deployment
finished. The run summary links to deployment status and the draft site. Avoid
repeated clicks while a build is running; cancelling the GitHub run cannot cancel
a request already sent to Netlify. No automatic POST retries are made.

See the [Pages CMS actions documentation](https://pagescms.org/docs/configuration/actions/).
