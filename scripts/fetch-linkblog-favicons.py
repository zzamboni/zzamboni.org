#!/usr/bin/env python3
"""Cache linked sites' favicons as local Hugo resources (no post edits)."""

import argparse
import hashlib
import io
import json
import os
import subprocess
import tomllib
import warnings
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

from cairosvg.surface import PNGSurface
from PIL import Image

ICON_DIR = Path("assets/img/linkblog-favicons")
MAX_BYTES = 2_000_000
Image.MAX_IMAGE_PIXELS = 4_000_000


def fetch(url):
    parsed = urlsplit(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username:
        raise ValueError("Expected an HTTP(S) URL without credentials")
    request = Request(url, headers={"User-Agent": "zzamboni.org-favicon/1.0"})
    with urlopen(request, timeout=15) as response:
        data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError("Response exceeds 2 MB")
        return data, response.geturl(), response.headers.get_content_charset() or "utf-8"


class IconLinks(HTMLParser):
    def __init__(self, url):
        super().__init__()
        self.base = url
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        href = attrs.get("href")
        if tag == "base" and href:
            self.base = urljoin(self.base, href)
        if tag == "link" and href:
            rel = (attrs.get("rel") or "").lower().split()
            if "icon" in rel or "apple-touch-icon" in rel:
                self.links.append(href)


def png_icon(data):
    # Decode raster formats (including ICO) before trying SVG. Re-encoding
    # strips metadata; the browser never receives downloaded SVG or scripts.
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            image = Image.open(io.BytesIO(data))
            image.load()
    except Image.UnidentifiedImageError:
        def no_external_resources(url, resource_type):
            raise ValueError("SVG favicon references an external resource")

        data = PNGSurface.convert(
            bytestring=data, output_width=96, output_height=96,
            unsafe=False, url_fetcher=no_external_resources,
        )
        image = Image.open(io.BytesIO(data))
        image.load()
    image = image.convert("RGBA")
    image.thumbnail((96, 96), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    image.save(output, format="PNG", optimize=True)
    return output.getvalue()


def discover_icon(url):
    parsed = urlsplit(url)
    origin = f"{parsed.scheme}://{parsed.netloc}/"
    candidates = []
    try:
        html, final_url, encoding = fetch(url)
        parser = IconLinks(final_url)
        parser.feed(html.decode(encoding, errors="replace"))
        candidates = [urljoin(parser.base, href) for href in parser.links]
        final = urlsplit(final_url)
        origin = f"{final.scheme}://{final.netloc}/"
    except Exception as error:
        print(f"Page metadata unavailable: {type(error).__name__}: {error}")
    # Conventional fallback works even when the article page blocks requests.
    candidates.append(urljoin(origin, "favicon.ico"))
    for candidate in list(dict.fromkeys(candidates))[:12]:
        try:
            data, _, _ = fetch(candidate)
            icon = png_icon(data)
            print(f"Fetched favicon: {candidate}")
            return icon
        except Exception as error:
            print(f"Icon unavailable: {candidate}: {type(error).__name__}: {error}")
    return None


def post_url(path):
    text = path.read_text()
    if not text.startswith("+++\n"):
        return None
    end = text.find("\n+++", 4)
    if end == -1:
        raise ValueError("Unclosed TOML frontmatter")
    return tomllib.loads(text[4:end]).get("externalUrl")


def changed_posts():
    before, after = os.getenv("BEFORE"), os.getenv("AFTER")
    if not before or not after or set(before) == {"0"}:
        return sorted(Path("content-pagescms").glob("*.md"))
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", "-z", "--diff-filter=AM", before, after],
    ).decode().split("\0")
    if any(name in ("scripts/fetch-linkblog-favicons.py",
                    ".github/workflows/fetch-linkblog-favicons.yml") for name in changed):
        return sorted(Path("content-pagescms").glob("*.md"))
    return [Path(name) for name in changed
            if Path(name).parent == Path("content-pagescms") and name.endswith(".md")]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("posts", nargs="*", help="Pages CMS Markdown paths; default: changed/all posts")
    parser.add_argument("--refresh", action="store_true", help="Refetch already cached icons")
    args = parser.parse_args()
    paths = [Path(name) for name in args.posts] if args.posts else changed_posts()
    print(f"Checking {len(paths)} posts")
    seen, updated = set(), []
    for path in paths:
        if path.parent != Path("content-pagescms") or path.suffix != ".md":
            raise ValueError(f"Expected a content-pagescms/*.md path: {path}")
        if not path.exists():
            print(f"Skipping deleted post: {path}")
            continue
        url = post_url(path)
        if not url:
            print(f"Skipping {path}: no externalUrl")
            continue
        parsed = urlsplit(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username:
            print(f"Skipping {path}: invalid externalUrl")
            continue
        host = parsed.netloc.lower()
        if host in seen:
            continue
        seen.add(host)
        # Must match sha256(lower $u.Host) in extend-article-link.html.
        destination = ICON_DIR / (hashlib.sha256(host.encode()).hexdigest() + ".png")
        if destination.exists() and not args.refresh:
            print(f"Cached favicon already present: {host}")
            continue
        print(f"Looking for favicon: {host} ({path})")
        icon = discover_icon(url)
        if icon is None:
            print(f"::warning::No usable favicon for {host}; keeping globe fallback")
            continue
        if destination.exists() and destination.read_bytes() == icon:
            print(f"Favicon unchanged: {host}")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(icon)
        updated.append(host)
    print(f"Updated {len(updated)} site icons")
    if output := os.getenv("GITHUB_OUTPUT"):
        subject = ", ".join(updated[:3])
        if len(updated) > 3:
            subject += f" and {len(updated) - 3} more sites"
        with open(output, "a") as stream:
            stream.write(f"subject={subject}\n")


if __name__ == "__main__":
    main()
