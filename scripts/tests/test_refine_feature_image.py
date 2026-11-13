import base64
import importlib.util
import io
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    "refine_feature_image", Path(__file__).parents[1] / "refine-feature-image-pr.py"
)
refine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refine)


class ImageAPIError(Exception):
    def __init__(self, status_code, code):
        super().__init__(code)
        self.status_code = status_code
        self.body = {"code": code}


@unittest.skipUnless(
    all(importlib.util.find_spec(module) for module in ("openai", "PIL", "yaml")),
    "Install openai, pillow and pyyaml to test feature images",
)
class RefineImageTests(unittest.TestCase):
    def setUp(self):
        from PIL import Image

        self.settings = refine.load_generation_settings()
        directory = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.source = directory / "current.webp"
        self.destination = directory / "refined.webp"
        Image.new("RGB", (16, 16), "red").save(self.source)
        self.client = self.enterContext(patch("openai.OpenAI")).return_value
        self.request = self.client.images.edit
        self.enterContext(patch.dict(os.environ, {}, clear=True))

        response = io.BytesIO()
        Image.new("RGBA", (16, 16), (255, 0, 0, 0)).save(response, "PNG")
        self.result = SimpleNamespace(data=[
            SimpleNamespace(b64_json=base64.b64encode(response.getvalue()).decode())
        ])
        self.request.return_value = self.result

    def edit(self):
        refine.edit_image(
            self.source, self.destination, "Make the background warmer",
            "Analog film photography", self.settings,
        )

    def requested_models(self):
        return [attempt.kwargs["model"] for attempt in self.request.call_args_list]

    def test_ordered_fallback_reuploads_image_and_preserves_edit_settings(self):
        from PIL import Image

        os.environ.update(
            FEATURE_IMAGE_MODELS=" preferred, preferred, second, third ",
            FEATURE_IMAGE_MODEL="legacy",
            FEATURE_IMAGE_SIZE="1024x1536",
            FEATURE_IMAGE_QUALITY="high",
        )
        uploads = []

        def respond(**kwargs):
            uploads.append(kwargs["image"].read())
            if len(uploads) < 3:
                raise ImageAPIError(404, "model_not_found")
            return self.result

        self.request.side_effect = respond
        self.edit()

        self.assertEqual(self.requested_models(), ["preferred", "second", "third"])
        self.assertEqual(uploads, [self.source.read_bytes()] * 3)
        for attempt in self.request.call_args_list:
            self.assertEqual(attempt.kwargs["size"], "1024x1536")
            self.assertEqual(attempt.kwargs["quality"], "high")
            self.assertEqual(attempt.kwargs["n"], 1)
            self.assertIn("Style: Analog film photography.", attempt.kwargs["prompt"])
            self.assertIn(self.settings.SITE_GUIDELINES, attempt.kwargs["prompt"])
            self.assertIn("Requested change: Make the background warmer", attempt.kwargs["prompt"])
        with Image.open(self.destination) as image:
            self.assertEqual((image.format, image.mode), ("WEBP", "RGB"))
            self.assertTrue(all(channel >= 250 for channel in image.getpixel((0, 0))))

    def test_blank_workflow_variables_use_defaults(self):
        os.environ.update(
            FEATURE_IMAGE_MODELS="", FEATURE_IMAGE_MODEL="",
            FEATURE_IMAGE_SIZE="", FEATURE_IMAGE_QUALITY="",
        )
        self.edit()
        self.assertEqual(self.requested_models(), [self.settings.DEFAULT_IMAGE_MODELS.split(",")[0]])
        self.assertEqual(self.request.call_args.kwargs["size"], "1536x1024")
        self.assertEqual(self.request.call_args.kwargs["quality"], "medium")

    def test_legacy_model_override(self):
        os.environ.update(FEATURE_IMAGE_MODELS="", FEATURE_IMAGE_MODEL="legacy")
        self.edit()
        self.assertEqual(self.requested_models(), ["legacy"])

    def test_unrelated_api_errors_stop_without_fallback(self):
        os.environ["FEATURE_IMAGE_MODELS"] = "first,second"
        for status, code in ((400, "invalid_image"), (429, "insufficient_quota")):
            with self.subTest(code=code):
                self.request.reset_mock()
                error = ImageAPIError(status, code)
                self.request.side_effect = error
                with self.assertRaises(ImageAPIError) as raised:
                    self.edit()
                self.assertIs(raised.exception, error)
                self.assertEqual(self.requested_models(), ["first"])
                self.assertFalse(self.destination.exists())

    def test_exhausted_models_report_failure_without_writing_image(self):
        os.environ["FEATURE_IMAGE_MODELS"] = "first,second"
        self.request.side_effect = ImageAPIError(403, "model_not_available")
        with self.assertRaisesRegex(RuntimeError, "No available image model among: first, second"):
            self.edit()
        self.assertEqual(self.requested_models(), ["first", "second"])
        self.assertFalse(self.destination.exists())
