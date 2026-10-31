"""Verify the ox-hugo link alias with Hugo's real shortcode renderer."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which('hugo'), 'Run under mise exec to provide Hugo')
class FigureLinkTests(unittest.TestCase):
    def test_link_alias(self):
        site = Path(tempfile.mkdtemp(prefix='zzamboni-figure-links-'))

        def put(path, text):
            target = site / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)

        try:
            put('hugo.toml', 'baseURL = "https://example.org/"\n')
            put('layouts/_default/single.html', '{{ .Content }}')
            put('layouts/shortcodes/figure.html', (ROOT / 'layouts/shortcodes/figure.html').read_text())
            put('layouts/partials/hugo-embedded/shortcodes/figure-default.html',
                (ROOT / 'themes/blowfish/layouts/partials/hugo-embedded/shortcodes/figure-default.html').read_text())
            cases = {
                'alias': ('link="https://example.org/destination" class="nozoom" caption="A caption"', 'https://example.org/destination'),
                'href': ('href="https://example.org/href"', 'https://example.org/href'),
                'both': ('href="https://example.org/href" link="https://example.org/link"', 'https://example.org/href'),
                'unlinked': ('', None),
                'default': ('default="true" link="https://example.org/default"', 'https://example.org/default'),
            }
            for name, (params, _) in cases.items():
                put(f'content/{name}.md', '+++\ntitle="Test"\n+++\n' +
                    '{{< figure src="https://example.org/image.png" ' + params + ' >}}')
            subprocess.run(['hugo', '--source', str(site)], check=True, capture_output=True, text=True)
            for name, (_, href) in cases.items():
                output = (site / 'public' / name / 'index.html').read_text()
                self.assertIn('src="https://example.org/image.png"', output)
                if href:
                    self.assertIn(f'href="{href}"', output)
                else:
                    self.assertNotIn('<a ', output)
            alias = (site / 'public/alias/index.html').read_text()
            self.assertIn('nozoom', alias)
            self.assertIn('<figcaption>A caption</figcaption>', alias)
        except Exception:
            print(f'Failed test artifacts retained at {site}')
            raise
        else:
            shutil.rmtree(site)
