#!/usr/bin/env python3
"""Refine the image in an AI feature-image PR from an owner's PR comment.

This script runs from the default branch. It reads only the image blob from the
PR head and never checks out or executes code from the PR branch.
"""

from __future__ import annotations

import base64
import importlib.util
import io
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


COMMAND = "/refine-image "
BRANCH_RE = re.compile(r"^ai-feature-image/([A-Za-z0-9][A-Za-z0-9._-]*)-([0-9]+)$")
STYLE_RE = re.compile(r"^Style: \*\*(.+?)\*\*\s*$", re.MULTILINE)
OWNER = "zzamboni"


def run(*args: str, input_text: str | None = None) -> str:
    result = subprocess.run(
        args, input=input_text, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


def validate(event: dict, pr: dict, changed_files: set[str], styles: dict) -> tuple[str, str, str, str]:
    comment = event["comment"]
    if comment["user"]["login"] != OWNER or not event["issue"].get("pull_request"):
        raise ValueError("Only the owner may refine a feature-image PR")
    body = comment["body"]
    if not body.startswith(COMMAND):
        raise ValueError("Expected a /refine-image command")
    instruction = body[len(COMMAND):].strip()
    if not instruction or len(instruction) > 2000:
        raise ValueError("Provide a refinement instruction of 1–2000 characters")

    repository = os.environ["GITHUB_REPOSITORY"]
    branch = pr["head"]["ref"]
    match = BRANCH_RE.fullmatch(branch)
    if (
        pr["state"] != "open"
        or pr["head"]["repo"]["full_name"] != repository
        or pr["base"]["repo"]["full_name"] != repository
        or pr["base"]["ref"] not in ("main", "staging")
        or not match
    ):
        raise ValueError("This is not an open, same-repository feature-image PR")

    slug = match.group(1)
    image_path = f"assets/img/generated/{slug}.webp"
    if image_path not in changed_files:
        raise ValueError(f"PR does not contain its generated image: {image_path}")

    style_match = STYLE_RE.search(pr.get("body") or "")
    style = style_match.group(1) if style_match else "Photographic editorial image"
    if style not in styles:
        raise ValueError(f"Unrecognized image style: {style}")
    return branch, image_path, instruction, style


def load_generation_settings():
    # Import trusted code from main to share the exact style definitions.
    path = Path(__file__).with_name("generate-feature-image.py")
    spec = importlib.util.spec_from_file_location("generate_feature_image", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def edit_image(source: Path, destination: Path, instruction: str, style: str, settings) -> None:
    from openai import OpenAI
    from PIL import Image

    with Image.open(source) as image:
        image.verify()

    prompt = (
        "Edit the supplied landscape feature image for a personal blog. "
        "Keep its central subject and composition recognizable. Make the requested "
        "change while retaining the chosen visual style and a clear focal point.\n\n"
        f"Style: {style}. {settings.IMAGE_STYLES[style]}\n\n"
        f"Shared guidelines: {settings.SITE_GUIDELINES}\n\n"
        f"Requested change: {instruction}"
    )
    with source.open("rb") as image:
        result = OpenAI().images.edit(
            model=os.getenv("FEATURE_IMAGE_MODEL", "gpt-image-1"),
            image=image,
            prompt=prompt,
            size=os.getenv("FEATURE_IMAGE_SIZE", "1536x1024"),
            quality=os.getenv("FEATURE_IMAGE_QUALITY", "medium"),
            n=1,
        )
    encoded = result.data[0].b64_json
    if not encoded:
        raise RuntimeError("Image edit returned no image")
    with Image.open(io.BytesIO(base64.b64decode(encoded))) as image:
        if image.mode == "RGBA":
            background = Image.new("RGB", image.size, "white")
            background.paste(image, mask=image.getchannel("A"))
            image = background
        elif image.mode != "RGB":
            image = image.convert("RGB")
        image.save(destination, "WEBP", quality=88, method=6)


def commit_image(head_sha: str, branch: str, image_path: str, image: Path, slug: str) -> str:
    # Use an isolated index to create a one-file commit without checking out PR code.
    with tempfile.TemporaryDirectory() as temp:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(temp) / "index"))

        def git(*args: str, input_text: str | None = None) -> str:
            return subprocess.run(
                ["git", *args], input=input_text, text=True, capture_output=True,
                env=env, check=True
            ).stdout.strip()

        blob = git("hash-object", "-w", str(image))
        git("read-tree", head_sha)
        git("update-index", "--add", "--cacheinfo", "100644", blob, image_path)
        tree = git("write-tree")
        commit = git(
            "-c", "user.name=github-actions[bot]",
            "-c", "user.email=41898282+github-actions[bot]@users.noreply.github.com",
            "commit-tree", tree, "-p", head_sha,
            input_text=f"auto: feature-image refine: {slug}\n",
        )
        # A concurrent change causes a non-fast-forward failure; do not overwrite it.
        git("push", "origin", f"{commit}:refs/heads/{branch}")
        return commit


def main() -> None:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    number = event["issue"]["number"]
    repository = os.environ["GITHUB_REPOSITORY"]
    pr = json.loads(run("gh", "api", f"repos/{repository}/pulls/{number}"))
    paths = run("gh", "api", f"repos/{repository}/pulls/{number}/files?per_page=100",
                "--paginate", "--jq", ".[].filename").splitlines()
    settings = load_generation_settings()
    branch, image_path, instruction, style = validate(
        event, pr, set(paths), settings.IMAGE_STYLES
    )

    run("git", "fetch", "--no-tags", "origin", f"refs/heads/{branch}")
    head_sha = run("git", "rev-parse", "FETCH_HEAD")
    if head_sha != pr["head"]["sha"]:
        raise RuntimeError("PR branch changed while preparing the edit; comment again to retry")

    with tempfile.TemporaryDirectory() as temp:
        source = Path(temp) / "current.webp"
        output = Path(temp) / "refined.webp"
        with source.open("wb") as fh:
            subprocess.run(["git", "show", f"{head_sha}:{image_path}"], stdout=fh, check=True)
        edit_image(source, output, instruction, style, settings)
        slug = Path(image_path).stem
        commit = commit_image(head_sha, branch, image_path, output, slug)

    run("gh", "issue", "comment", str(number), "--body",
        f"Updated the image using your refinement instruction ({style}). "
        f"Revision: {commit[:12]}. The Deploy Preview will update shortly.")


if __name__ == "__main__":
    main()
