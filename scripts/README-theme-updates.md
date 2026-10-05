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
