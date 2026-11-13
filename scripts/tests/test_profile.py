"""Exercise the profile shortcode with Hugo's real image processing."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which('hugo'), 'Run under mise exec to provide Hugo')
class ProfileTests(unittest.TestCase):
    def test_image_variants(self):
        site = Path(tempfile.mkdtemp(prefix='zzamboni-profile-'))

        def put(path, text):
            target = site / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)

        try:
            put('layouts/_default/single.html', '{{ .Content }}')
            put('layouts/shortcodes/profile.html',
                (ROOT / 'layouts/shortcodes/profile.html').read_text())
            put('layouts/partials/author-links.html', '<a href="/links/">Links</a>')
            put('content/about.md', '+++\ntitle="About"\n+++\n{{< profile >}}')
            put('assets/avatar.svg', '<svg xmlns="http://www.w3.org/2000/svg" '
                'width="100" height="100"><circle cx="50" cy="50" r="45"/></svg>')
            shutil.copyfile(ROOT / 'assets/img/avatar.jpg', site / 'assets/avatar.jpg')
            for image, disabled in [('avatar.jpg', False), ('avatar.jpg', True),
                                    ('avatar.svg', False), ('missing.jpg', False)]:
                with self.subTest(image=image, disabled=disabled):
                    put('hugo.toml', 'baseURL="https://example.org/"\n[params]\n'
                        f'disableImageOptimization={str(disabled).lower()}\n'
                        f'[params.author]\nname="Test Author"\nimage="{image}"\n')
                    subprocess.run(['hugo', '--source', str(site)], check=True,
                                   capture_output=True, text=True)
                    output = (site / 'public/about/index.html').read_text()
                    self.assertIn('Test Author', output)
                    self.assertIn('href="/links/"', output)
                    if image == 'missing.jpg':
                        self.assertNotIn('<img', output)
                        continue
                    self.assertIn('loading="eager"', output)
                    self.assertIn('fetchpriority="high"', output)
                    self.assertIn(f'data-zoom-src="/{image}"', output)
                    src = re.search(r'\ssrc="([^"]+)"', output)[1]
                    if disabled or image.endswith('.svg'):
                        self.assertEqual(src, '/' + image)
                    else:
                        self.assertNotEqual(src, '/' + image)
                        self.assertTrue((site / 'public' / src.lstrip('/')).is_file())
        except Exception:
            print(f'Profile test artifacts retained at {site}')
            raise
        else:
            shutil.rmtree(site)
