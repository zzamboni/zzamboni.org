"""Run with mise exec -- python3 -m unittest discover -s scripts/tests -p test_archive.py."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which('hugo'), 'Run under mise exec to provide Hugo')
class ArchiveTests(unittest.TestCase):
    def test_archive_scope_order_and_drafts(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)

            def put(path, text):
                target = site / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text)

            put('hugo.toml', '''baseURL = "https://example.org/"
[pagination]
pagerSize = 1
[module]
[[module.mounts]]
source = "content"
target = "content"
[[module.mounts]]
source = "content-pagescms"
target = "content/post"
[[module.mounts]]
source = "content-legacy"
target = "content/post"
''')
            for path in ['content/archive/_index.md', 'layouts/_default/archive.html',
                         'layouts/partials/archive-list.html',
                         'layouts/partials/archive-chart.html', 'i18n/en.yaml']:
                put(path, (ROOT / path).read_text())
            put('layouts/_default/baseof.html', '{{ block "main" . }}{{ end }}')
            put('layouts/_default/single.html', '{{ define "main" }}{{ .Content }}{{ end }}')
            fixtures = [
                ('content/post/old/index.md', 'Old article', '2020-01-01', ''),
                ('content-pagescms/new.md', 'New article', '2025-01-02', ''),
                ('content-legacy/link.md', 'External link', '2025-01-03', 'externalUrl = "https://example.com/story"'),
                ('content/post/photo.md', 'Photo excluded', '2025-01-04', 'tags = ["photos"]'),
                ('content/post/draft.md', 'Draft article', '2025-01-05', 'draft = true'),
                ('content/post/undated.md', 'Undated draft', None, 'draft = true'),
                ('content/about.md', 'About excluded', '2025-01-06', ''),
            ]
            for path, title, date, extra in fixtures:
                date_field = f'date = {date}\n' if date else ''
                put(path, f'+++\ntitle = "{title}"\n{date_field}{extra}\n+++\nBody')
            for draft in [False, True]:
                destination = site / ('draft-output' if draft else 'production-output')
                command = ['hugo', '--source', str(site), '--destination', str(destination)]
                if draft:
                    command.append('--buildDrafts')
                subprocess.run(command, check=True, capture_output=True, text=True)
                html = (destination / 'archive/index.html').read_text()
                for title in ['Old article', 'New article', 'External link']:
                    self.assertIn(title, html)
                for title in ['Photo excluded', 'About excluded']:
                    self.assertNotIn(title, html)
                self.assertEqual('Draft article' in html, draft)
                self.assertEqual('Undated draft' in html, draft)
                chart = html.split('<nav class="archive-chart"', 1)[1].split('</nav>', 1)[0]
                years = re.findall(r'class="archive-chart-year"[^>]*>(\d+)</span>', chart)
                self.assertEqual(years, [str(year) for year in range(2020, 2026)])
                counts = re.findall(r'class="archive-chart-count">(\d+)</span>', chart)
                self.assertEqual(counts, ['1', '0', '0', '0', '0', '3' if draft else '2'])
                heights = re.findall(r'style="height: ([\d.]+)%"', chart)
                self.assertEqual(len(heights), 2)
                self.assertAlmostEqual(float(heights[0]), 100 / (3 if draft else 2), places=4)
                self.assertEqual(float(heights[1]), 100)
                self.assertLess(html.index('External link'), html.index('New article'))
                self.assertLess(html.index('New article'), html.index('Old article'))
                self.assertIn('href="#year-2025"', html)
                self.assertIn('id="year-2025"', html)
                self.assertIn(f'({3 if draft else 2})', html)
                self.assertIn('href="https://example.com/story" rel="external"', html)
                self.assertIn('class="archive-badge">Link</span>', html)
                self.assertIn('datetime="2025-01-03"', html)
                self.assertNotIn('<img', html)
                self.assertFalse((destination / 'archive/page/2').exists())
            # Empty content has no orphan year navigation or sections.
            for path, *_ in fixtures:
                (site / path).unlink()
            destination = site / 'empty-output'
            subprocess.run(['hugo', '--source', str(site), '--destination', str(destination)],
                           check=True, capture_output=True, text=True)
            self.assertNotIn('class="archive-chart"', (destination / 'archive/index.html').read_text())
            # An archive containing only undated drafts must not draw a year-1 chart.
            put('content/post/undated.md', '+++\ntitle = "Undated only"\ndraft = true\n+++\nBody')
            subprocess.run(['hugo', '--source', str(site), '--destination', str(destination),
                            '--buildDrafts'], check=True, capture_output=True, text=True)
            html = (destination / 'archive/index.html').read_text()
            self.assertIn('Undated only', html)
            self.assertNotIn('class="archive-chart"', html)
