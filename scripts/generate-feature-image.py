#!/usr/bin/env python3
"""Generate AI feature images for Hugo posts.

The generated Hugo Markdown is used as the common input for both Pages CMS and
Org/ox-hugo posts.  Metadata is written back to the canonical source when it can
be identified, while also updating the rendered Markdown so a deploy preview can
show the result immediately.
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import re
import sys
import tomllib
import urllib.request
from pathlib import Path
from typing import Any

import yaml
from openai import OpenAI
from PIL import Image


DEFAULT_FEATURE_IMAGES = {
    "img/tram-zurich.jpg",
    "/img/tram-zurich.jpg",
    "images/tram-zurich.jpg",
    "/images/tram-zurich.jpg",
}
FEATURE_KEYS = ("featureimage", "featured_image", "featureImage")
ORG_SOURCE = Path("content-org/zzamboni.org")
GENERATED_DIR = Path("assets/img/generated")

SITE_STYLE = """Create a landscape editorial illustration for a personal technical blog.
Clean, understated, intelligent, and slightly playful. Use natural or believable
lighting, a restrained composition, and a strong focal point that remains clear
at thumbnail size. Do not include visible text, captions, logos, watermarks, UI
labels, or decorative typography. Avoid generic corporate stock-art aesthetics,
neon cyberpunk imagery, floating code, and gratuitous circuit-board motifs."""


def parse_frontmatter(path: Path) -> tuple[str, dict[str, Any], str, str]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("+++\n"):
        marker = "+++"
        end = text.find("\n+++\n", 4)
        if end < 0:
            raise ValueError(f"{path}: unterminated TOML front matter")
        raw = text[4:end]
        return "toml", tomllib.loads(raw), raw, text[end + 5 :]

    if text.startswith("---\n"):
        marker = "---"
        end = text.find("\n---\n", 4)
        if end < 0:
            raise ValueError(f"{path}: unterminated YAML front matter")
        raw = text[4:end]
        return "yaml", yaml.safe_load(raw) or {}, raw, text[end + 5 :]

    raise ValueError(f"{path}: unsupported or missing front matter")


def feature_image(frontmatter: dict[str, Any]) -> str:
    for key in FEATURE_KEYS:
        value = frontmatter.get(key)
        if value:
            return str(value).strip()
    return ""


def is_candidate(frontmatter: dict[str, Any], force: bool = False) -> bool:
    if force:
        return True
    current = feature_image(frontmatter)
    return not current or current in DEFAULT_FEATURE_IMAGES


def page_slug(path: Path, frontmatter: dict[str, Any]) -> str:
    slug = str(frontmatter.get("slug", "")).strip()
    if slug:
        return slug.strip("/")
    if path.name == "index.md":
        return path.parent.name
    return path.stem


def update_frontmatter_text(path: Path, image_path: str) -> None:
    kind, _frontmatter, raw, body = parse_frontmatter(path)
    replacement_key = "featureimage"

    # Preserve the file's existing formatting rather than reserializing all front matter.
    key_re = re.compile(
        r"(?m)^(?P<indent>\s*)(?:featureimage|featured_image|featureImage)\s*[:=].*$"
    )

    if kind == "toml":
        replacement = f'{replacement_key} = {json.dumps(image_path)}'
        if key_re.search(raw):
            raw = key_re.sub(lambda m: m.group("indent") + replacement, raw, count=1)
        else:
            raw = raw.rstrip() + "\n" + replacement
        path.write_text("+++\n" + raw + "\n+++\n" + body, encoding="utf-8")
    else:
        replacement = f"{replacement_key}: {image_path}"
        if key_re.search(raw):
            raw = key_re.sub(lambda m: m.group("indent") + replacement, raw, count=1)
        else:
            raw = raw.rstrip() + "\n" + replacement
        path.write_text("---\n" + raw + "\n---\n" + body, encoding="utf-8")


def find_org_drawer(slug: str) -> tuple[list[str], int, int] | None:
    if not ORG_SOURCE.exists():
        return None

    lines = ORG_SOURCE.read_text(encoding="utf-8").splitlines()
    target = slug.strip("/")

    for i, line in enumerate(lines):
        m = re.match(
            r"^:(export_hugo_bundle|export_file_name):\s*(.*?)\s*$",
            line,
            flags=re.IGNORECASE,
        )
        if not m:
            continue

        value = m.group(2).strip().strip('"')
        if value != target:
            continue

        start = i
        while start >= 0 and lines[start].strip().upper() != ":PROPERTIES:":
            start -= 1
        end = i
        while end < len(lines) and lines[end].strip().upper() != ":END:":
            end += 1

        if start >= 0 and end < len(lines):
            return lines, start, end

    return None


def update_org_source(slug: str, image_path: str) -> bool:
    found = find_org_drawer(slug)
    if not found:
        return False

    lines, start, end = found
    prop_index = None
    for i in range(start + 1, end):
        if re.match(
            r"^:export_hugo_custom_front_matter:",
            lines[i],
            flags=re.IGNORECASE,
        ):
            prop_index = i
            break

    if prop_index is None:
        lines.insert(end, f":export_hugo_custom_front_matter: :featureimage {image_path}")
    else:
        line = lines[prop_index]
        if re.search(r":(?:featureimage|featured_image)\s+\S+", line, flags=re.IGNORECASE):
            line = re.sub(
                r":(?:featureimage|featured_image)\s+\S+",
                f":featureimage {image_path}",
                line,
                count=1,
                flags=re.IGNORECASE,
            )
        else:
            line = line.rstrip() + f" :featureimage {image_path}"
        lines[prop_index] = line

    ORG_SOURCE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def clean_body(body: str, limit: int = 14000) -> str:
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.DOTALL)
    body = re.sub(r"\s+", " ", body).strip()
    return body[:limit]


def make_visual_brief(
    client: OpenAI,
    title: str,
    summary: str,
    tags: list[str],
    body: str,
    extra_prompt: str,
) -> str:
    model = os.getenv("FEATURE_IMAGE_TEXT_MODEL", "gpt-5-mini")
    response = client.responses.create(
        model=model,
        store=False,
        instructions=(
            "Create a concise visual brief for an editorial feature image inspired by "
            "a personal technical blog post. Focus on the post's central idea rather "
            "than literal screenshots. Specify subject, visual emphasis, composition, "
            "mood/style, and what to avoid. No visible text or logos. Return only the brief."
        ),
        input=(
            f"Title: {title}\n"
            f"Summary: {summary}\n"
            f"Tags: {', '.join(tags)}\n"
            f"Optional direction: {extra_prompt}\n\n"
            f"Post:\n{clean_body(body)}"
        ),
    )
    return response.output_text.strip()


def generate_image(client: OpenAI, prompt: str, destination: Path) -> None:
    model = os.getenv("FEATURE_IMAGE_MODEL", "gpt-image-1")
    size = os.getenv("FEATURE_IMAGE_SIZE", "1536x1024")
    quality = os.getenv("FEATURE_IMAGE_QUALITY", "medium")

    result = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        n=1,
    )
    item = result.data[0]

    if getattr(item, "b64_json", None):
        raw = base64.b64decode(item.b64_json)
    elif getattr(item, "url", None):
        with urllib.request.urlopen(item.url, timeout=60) as response:
            raw = response.read()
    else:
        raise RuntimeError("Image API returned neither b64_json nor a URL")

    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(io.BytesIO(raw)) as image:
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")
        if image.mode == "RGBA":
            background = Image.new("RGB", image.size, "white")
            background.paste(image, mask=image.getchannel("A"))
            image = background
        image.save(destination, "WEBP", quality=88, method=6)


def generate(post: Path, extra_prompt: str, force: bool) -> None:
    kind, frontmatter, _raw, body = parse_frontmatter(post)
    if not is_candidate(frontmatter, force=force):
        raise SystemExit(
            f"{post} already has feature image {feature_image(frontmatter)!r}; "
            "use --force to replace it"
        )

    title = str(frontmatter.get("title", "")).strip()
    if not title:
        raise SystemExit(f"{post}: no title found")

    summary = str(frontmatter.get("summary", frontmatter.get("description", ""))).strip()
    tags_value = frontmatter.get("tags", [])
    if isinstance(tags_value, str):
        tags = [tags_value]
    else:
        tags = [str(tag) for tag in tags_value or []]

    slug = page_slug(post, frontmatter)
    output = GENERATED_DIR / f"{slug}.webp"
    hugo_path = f"img/generated/{slug}.webp"

    client = OpenAI()
    brief = make_visual_brief(client, title, summary, tags, body, extra_prompt)
    full_prompt = SITE_STYLE + "\n\nVisual brief:\n" + brief

    print(f"Post: {post}")
    print(f"Output: {output}")
    print("\nVisual brief:\n" + brief + "\n")

    generate_image(client, full_prompt, output)

    # Pages CMS files and legacy Markdown are canonical themselves.  ox-hugo
    # Markdown is regenerated from Org, so update both the Org property and the
    # current Markdown output for an immediate deploy preview.
    update_frontmatter_text(post, hugo_path)

    org_updated = False
    creator = str(frontmatter.get("creator", "")).lower()
    if "ox-hugo" in creator or post.as_posix().startswith("content/post/"):
        org_updated = update_org_source(slug, hugo_path)

    if org_updated:
        print(f"Updated canonical Org metadata in {ORG_SOURCE}")
    else:
        print("No matching Org entry found; treated Markdown as canonical source")

    github_output = os.getenv("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as fh:
            fh.write(f"slug={slug}\n")
            fh.write(f"title={title}\n")
            fh.write(f"image={hugo_path}\n")


def candidates(limit: int | None) -> None:
    paths: list[Path] = []
    for root in (Path("content-pagescms"), Path("content/post")):
        if root.exists():
            paths.extend(root.rglob("*.md"))

    count = 0
    for path in sorted(paths):
        if path.name == "_index.md":
            continue
        try:
            _kind, frontmatter, _raw, _body = parse_frontmatter(path)
        except Exception:
            continue
        if is_candidate(frontmatter):
            print(path)
            count += 1
            if limit is not None and count >= limit:
                break


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_generate = sub.add_parser("generate", help="generate one feature image")
    p_generate.add_argument("post", type=Path)
    p_generate.add_argument("--extra-prompt", default="")
    p_generate.add_argument("--force", action="store_true")

    p_candidates = sub.add_parser(
        "candidates", help="list posts with no image or the default tram image"
    )
    p_candidates.add_argument("--limit", type=int)

    args = parser.parse_args()

    if args.command == "generate":
        generate(args.post, args.extra_prompt, args.force)
    else:
        candidates(args.limit)


if __name__ == "__main__":
    main()
