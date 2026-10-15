"""Render the real related partial against a small, isolated Hugo content set.

Run with: mise exec -- python3 -m unittest discover -s scripts/tests -p test_related_content.py
"""
from pathlib import Path
import json
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which('hugo'), 'Run under mise exec to provide Hugo')
class RelatedContentTests(unittest.TestCase):
    def test_article_only_recommendations(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)

            def put(path, text):
                target = site / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text)

            related_config = (ROOT / 'config/_default/hugo.toml').read_text().split('[related]', 1)[1]
            put('hugo.toml', '''baseURL = "https://example.org/"
[params.article]
showRelatedContent = true
relatedContentLimit = 3
[module]
[[module.mounts]]
source = "content"
target = "content"
[[module.mounts]]
source = "content-pagescms"
target = "content/post"
[related]
''' + related_config)
            put('layouts/_default/single.html', '{{ partial "related.html" . }}')
            put('layouts/partials/related.html', (ROOT / 'layouts/partials/related.html').read_text())
            put('layouts/partials/article-link/card-related.html', '<a href="{{ .RelPermalink }}">{{ .Title }}</a>')
            put('i18n/en.yaml', 'article:\n  related_articles: Related articles\n')
            fixtures = {
                'content/post/org/index.md': ('Org', '2020-01-01', ['Hugo'], ''),
                'content-pagescms/cms.md': ('CMS', '2026-01-01', ['hugo'], ''),
                'content/post/link.md': ('Link', '2025-01-01', ['hugo'], 'externalUrl = "https://example.org/link"'),
                'content/post/photo.md': ('Photo', '2025-01-01', ['hugo', 'photos'], ''),
                'content/post/gallery.md': ('Gallery', '2025-01-01', ['hugo'], 'photos = ["image.jpg"]'),
                'content/post/unrelated.md': ('Unrelated', '2025-01-01', ['unique'], ''),
                'content/about.md': ('About', '2025-01-01', ['hugo'], ''),
                'content/post/optout.md': ('Optout', '2025-01-01', ['hugo'], 'showRelatedContent = false'),
                'content/post/draft.md': ('Draft', '2025-01-01', ['hugo'], 'draft = true'),
            }
            for path, (title, date, tags, extra) in fixtures.items():
                put(path, f'+++\ntitle = "{title}"\ndate = {date}\ntags = {json.dumps(tags)}\n{extra}\n+++\nBody')
            subprocess.run(['hugo', '--source', str(site)], check=True, capture_output=True, text=True)
            output = site / 'public'
            org = (output / 'post/org/index.html').read_text()
            cms = (output / 'post/cms/index.html').read_text()
            self.assertIn('>CMS</a>', org)  # Newer, differently cased tag, mounted CMS source.
            self.assertIn('>Org</a>', cms)
            self.assertNotIn('>Org</a>', org)
            self.assertNotIn('>CMS</a>', cms)
            for title in ['Link', 'Photo', 'Gallery', 'About', 'Draft', 'Unrelated']:
                self.assertNotIn(f'>{title}</a>', org)
            self.assertLessEqual(org.count('<a '), 3)
            for path in ['post/link', 'post/photo', 'post/gallery', 'post/unrelated', 'about', 'post/optout']:
                self.assertNotIn('related-articles-title', (output / path / 'index.html').read_text())
            config = site / 'hugo.toml'
            config.write_text(config.read_text().replace('relatedContentLimit = 3', 'relatedContentLimit = 1'))
            subprocess.run(['hugo', '--source', str(site)], check=True, capture_output=True, text=True)
            self.assertEqual((output / 'post/org/index.html').read_text().count('<a '), 1)
