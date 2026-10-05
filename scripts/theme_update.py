#!/usr/bin/env python3
"""Reviewable Blowfish/Hugo updates. Requires Python 3.11+, git, and mise."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import tomllib
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "themes/blowfish"
MISE = ROOT / "mise.toml"
NETLIFY = ROOT / "netlify.toml"


def run(*args, cwd=ROOT, env=None):
    return subprocess.check_output(args, cwd=cwd, env=env, text=True).strip()


def version(value):
    if not re.fullmatch(r"v?\d+\.\d+\.\d+", value):
        raise ValueError(f"Not a stable version: {value}")
    return tuple(map(int, value.removeprefix("v").split(".")))


def get_json(url):
    headers = {"User-Agent": "zzamboni-theme-updater"}
    if token := os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        return json.load(response)


def releases(repo):
    page = 1
    while True:
        batch = get_json(f"https://api.github.com/repos/{repo}/releases?per_page=100&page={page}")
        if not batch:
            return
        for release in batch:
            tag = release["tag_name"]
            if not release["draft"] and not release["prerelease"] and re.fullmatch(r"v?\d+\.\d+\.\d+", tag):
                yield tag
        page += 1


def bounds(ref="HEAD"):
    config = tomllib.loads(run("git", "show", f"{ref}:config.toml", cwd=THEME))
    limits = config["module"]["hugoVersion"]
    return version(limits["min"]), version(limits["max"])


def pin():
    return tomllib.loads(MISE.read_text())["tools"]["hugo-extended"]


def synced_texts(hugo):
    mise, count = re.subn(r'(?m)^hugo-extended\s*=\s*"[^"]+"', f'hugo-extended = "{hugo}"', MISE.read_text())
    if count != 1:
        raise ValueError("Expected exactly one hugo-extended pin in mise.toml")
    netlify, count = re.subn(r'(?m)^(\s*HUGO_VERSION\s*=\s*)"[^"]+"', rf'\g<1>"{hugo}"', NETLIFY.read_text())
    if not count:
        raise ValueError("No Netlify Hugo pins found")
    return mise, netlify


def verify():
    hugo = pin()
    low, high = bounds()
    if not low <= version(hugo) <= high:
        raise ValueError("mise Hugo pin is outside the checked-out theme's supported range")
    _, expected = synced_texts(hugo)
    if expected != NETLIFY.read_text():
        raise ValueError("Netlify Hugo pins differ from mise.toml")
    tool = f"hugo-extended@{hugo}"
    run("mise", "install", tool)
    actual = run("mise", "exec", tool, "--", "hugo", "version")
    if not re.search(r"\bv" + re.escape(hugo) + r"(?:-|\+)", actual) or "+extended" not in actual:
        raise ValueError(f"Unexpected Hugo binary: {actual}")
    output = Path(tempfile.mkdtemp(prefix="zzamboni-theme-build-"))
    env = dict(os.environ, HUGO_RESOURCEDIR=str(output / "resources"))
    print(actual, flush=True)
    print(run("mise", "exec", tool, "--", "hugo", "--gc", "--minify",
              "--environment", "production", "--destination", str(output / "public"),
              "--cacheDir", str(output / "cache"), env=env))
    print(f"Build output: {output / 'public'}")


def report(old, new):
    upstream = set(run("git", "ls-tree", "-r", "--name-only", old, "layouts", cwd=THEME).splitlines())
    upstream.update(run("git", "ls-tree", "-r", "--name-only", new, "layouts", cwd=THEME).splitlines())
    entries = [{"local": str(p.relative_to(ROOT)), "upstream": str(p.relative_to(ROOT)),
                "reason": "Same-path site override"}
               for p in (ROOT / "layouts").rglob("*") if p.is_file() and str(p.relative_to(ROOT)) in upstream]
    entries += tomllib.loads((ROOT / "scripts/theme-overrides.toml").read_text())["overrides"]
    directory = Path(tempfile.mkdtemp(prefix="zzamboni-theme-review-"))
    notes = [f"Theme update: {old} -> {new}\n"]
    for entry in entries:
        diff = run("git", "diff", old, new, "--", entry["upstream"], cwd=THEME)
        notes.append(f"{'REVIEW' if diff else 'unchanged'}: {entry['local']} <- {entry['upstream']} ({entry['reason']})")
        if diff:
            (directory / (entry["upstream"].replace("/", "__") + ".diff")).write_text(diff + "\n")
    # Also retain the complete layout diff to expose changes in transitive partials.
    (directory / "all-layouts.diff").write_text(run("git", "diff", old, new, "--", "layouts", cwd=THEME) + "\n")
    (directory / "README.txt").write_text("\n".join(notes) + "\n")
    print("\n".join(notes))
    print(f"Review files: {directory}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["check", "update", "verify"])
    args = parser.parse_args()
    if args.action == "verify":
        verify()
        return
    if run("git", "status", "--porcelain", cwd=THEME):
        raise ValueError("Theme has local changes; commit or stash them first")
    latest = max(releases("nunocoracao/blowfish"), key=version)
    # Fetch tags explicitly; never follow unreleased main for an update.
    run("git", "fetch", "origin", "--tags", cwd=THEME)
    old = run("git", "rev-parse", "HEAD", cwd=THEME)
    low, high = bounds(latest)
    compatible = [tag for tag in releases("gohugoio/hugo") if low <= version(tag) <= high]
    if not compatible:
        raise ValueError(f"No stable Hugo release in range {low}..{high}")
    hugo = max(compatible, key=version).removeprefix("v")
    print(f"Blowfish: {run('git', 'describe', '--tags', '--always', cwd=THEME)} -> {latest}")
    print(f"Hugo extended: {pin()} -> {hugo}")
    mise, netlify = synced_texts(hugo)
    print(f"Netlify pins: {'in sync' if netlify == NETLIFY.read_text() else 'need synchronization'}")
    report(old, latest)
    if args.action == "check":
        return
    dirty = run("git", "status", "--porcelain", "--", "mise.toml", "netlify.toml", "themes/blowfish")
    if dirty:
        raise ValueError("Commit or stash changes to version files/submodule before updating:\n" + dirty)
    run("git", "switch", "--detach", latest, cwd=THEME)
    MISE.write_text(mise)
    NETLIFY.write_text(netlify)
    print("Updated pins. Changes remain uncommitted; review template diffs even if the build passes.", flush=True)
    verify()


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"Theme workflow failed: {exc}\nAny applied changes remain available for review.")
