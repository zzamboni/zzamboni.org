# Theme and Hugo updates

Requires Python 3.11+, Git, mise, and network access to GitHub. The source of
truth for Hugo is `[tools].hugo-extended` in `mise.toml`. `mise run serve` uses
that version without changing Homebrew. Activate mise in your shell if you
also want plain `hugo` commands to use the repository pin.

```sh
mise run theme-check
mise run theme-update
mise run theme-verify
```

`theme-check` fetches release metadata and Git tags, selects the highest stable
Blowfish release and highest stable Hugo release inside its declared range,
and reports pin drift. It does not change the checkout or configuration.
Set `GH_TOKEN` or `GITHUB_TOKEN` if GitHub API rate limits affect you.

`theme-update` requires clean version files and a clean theme submodule. It
checks out the release, synchronizes every Netlify Hugo pin, installs Hugo
Extended through mise, and builds into a printed temporary directory. It
does not commit, push, deploy, or edit templates. If installation/build fails,
changes remain visible for diagnosis; rerun `theme-verify` after fixing them.

Review the printed override report and `.diff` files. Matching layout paths
are discovered automatically; indirect dependencies are recorded in
`scripts/theme-overrides.toml`. `all-layouts.diff` covers upstream changes to
other partials too. Merge relevant changes manually while preserving local
behavior, then run `theme-verify` and visually inspect `mise run serve`.
Keep the temporary report until review is complete. A successful build is not
proof that the custom layout still looks or behaves correctly.

Commit the theme pointer, version pins, and any override changes together.
`blowfish-upgrade` is an alias for the new workflow. The old `update-hugo.elv`
now delegates to it rather than copying the Homebrew version and committing.

Offline logic tests: `python3 -m unittest discover -s scripts/tests`.

## JSON Resume module updates

For a local update, run `mise run jsonresume-update`; its default revision is
the renderer's `main` branch. Pass a tag or commit as an argument to select a
specific revision. Review and commit the resulting `go.mod`/`go.sum` changes.

For a review PR, open **Actions > Update JSON Resume module > Run workflow**
and choose `main` or `staging`. The selected branch is the PR's base. The
workflow must first reach the default branch (`main`) to appear in GitHub's
manual-run UI; after that, select `staging` there to test updates against it.

The workflow resolves the latest upstream `main` commit once (rather than
Go's latest tagged release), creates a unique update branch, runs the same
mise task with that commit, and builds the site with drafts included. It
commits only `go.mod` and `go.sum`, using an `auto: jsonresume:` subject, then
opens a PR with the old/new versions and upstream comparison links. An
already-current pin creates no remote branch or PR; a failed build stops
before pushing. Re-running a changed update creates a new PR, so close any
older proposal it replaces.

The workflow uses the repository's `GITHUB_TOKEN` with contents and pull-request
write permissions, matching the feature-image workflow. Repository Actions
settings must allow GitHub Actions to create pull requests. No new secret is
required. PR creation does not trigger other GitHub Actions workflows with
this token; Netlify deploy previews use the existing GitHub integration.
The module files are site-relevant to the Netlify build filter. Preview builds
still depend on the project's deploy-preview settings and are skipped if that
project enables `NETLIFY_ON_DEMAND=true` without a force-build override.

Before merging, review `/vita/` and `/vita/publications/` in the PR's Netlify
preview, including mobile layout and light/dark appearance. The workflow does
not auto-merge, refresh CV data, or request a production/draft-site build hook.
