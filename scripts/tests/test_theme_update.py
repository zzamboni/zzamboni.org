import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("theme_update", Path(__file__).parents[1] / "theme_update.py")
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)


class VersionTests(unittest.TestCase):
    def test_numeric_versions_and_prereleases(self):
        self.assertGreater(workflow.version("v0.166.0"), workflow.version("0.99.0"))
        with self.assertRaises(ValueError):
            workflow.version("v0.167.0-rc1")

    def test_release_pagination_filters_unstable(self):
        with patch.object(workflow, "get_json", side_effect=[[
            dict(tag_name="v1.0.0", draft=False, prerelease=False),
            dict(tag_name="v2.0.0", draft=False, prerelease=True),
            dict(tag_name="v3.0.0", draft=True, prerelease=False),
        ], [dict(tag_name="v0.9.0", draft=False, prerelease=False)], []]):
            self.assertEqual(list(workflow.releases("example/repo")), ["v1.0.0", "v0.9.0"])

    def test_sync_preserves_other_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            mise, netlify = Path(directory) / "mise.toml", Path(directory) / "netlify.toml"
            mise.write_text('[tools]\nhugo-extended = "0.164.0"\n# keep\n')
            netlify.write_text('[build.environment]\nHUGO_VERSION = "0.164.0"\nTZ = "CET"\n[context.production.environment]\n  HUGO_VERSION = "0.165.0"\n')
            with patch.object(workflow, "MISE", mise), patch.object(workflow, "NETLIFY", netlify):
                m, n = workflow.synced_texts("0.166.0")
            self.assertIn("# keep", m)
            self.assertIn('TZ = "CET"', n)
            self.assertEqual(n.count('"0.166.0"'), 2)
            self.assertIn("0.164.0", mise.read_text())
