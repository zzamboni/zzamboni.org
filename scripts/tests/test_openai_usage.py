import importlib.util
import os
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import patch
from pathlib import Path
from io import StringIO

spec = importlib.util.spec_from_file_location('usage', Path(__file__).parents[1] / 'openai-usage.py')
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)
NOW = datetime(2026, 10, 7, 12, tzinfo=timezone.utc)


class UsageTests(unittest.TestCase):
    def test_missing_metadata(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(usage, 'costs', return_value=Decimal('0.03')):
            result = usage.report(NOW, 'test')
        self.assertIn('| Today | $0.0300 |', result)
        self.assertIn('| Month to date | $0.0300 |', result)
        self.assertNotIn('Estimated remaining credit:', result)

    def test_reload_and_expiry(self):
        with patch.dict(os.environ, {'OPENAI_CREDIT_DATE': '2026-10-01', 'OPENAI_CREDIT_AMOUNT': '5'}, clear=True), patch.object(usage, 'costs', return_value=Decimal('0.25')):
            result = usage.report(NOW, 'test')
        self.assertIn('**$4.7500**', result)
        self.assertIn('**2027-10-01**', result)

    def test_expired_credit(self):
        with patch.dict(os.environ, {'OPENAI_CREDIT_DATE': '2025-10-01', 'OPENAI_CREDIT_AMOUNT': '5'}, clear=True), patch.object(usage, 'costs', return_value=Decimal('0.25')):
            result = usage.report(NOW, 'test')
        self.assertIn('**$0.0000**', result)
        self.assertIn('has expired', result)

    def test_invalid_amount_keeps_usage_and_expiry(self):
        with patch.dict(os.environ, {'OPENAI_CREDIT_DATE': '2026-10-01', 'OPENAI_CREDIT_AMOUNT': 'NaN'}, clear=True), patch.object(usage, 'costs', return_value=Decimal('0.25')):
            result = usage.report(NOW, 'test')
        self.assertIn('| Month to date | $0.2500 |', result)
        self.assertIn('**2027-10-01**', result)
        self.assertNotIn('Estimated remaining credit:', result)

    def test_leap_day(self):
        with patch.dict(os.environ, {'OPENAI_CREDIT_DATE': '2024-02-29'}, clear=True):
            _, expiry, _, _ = usage.reload_metadata(NOW)
        self.assertEqual(str(expiry.date()), '2025-02-28')

    def test_api_failure(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(usage, 'costs', side_effect=TimeoutError()):
            result = usage.report(NOW, 'test')
        self.assertIn('| Today | Unavailable |', result)
        self.assertIn('| Month to date | Unavailable |', result)

    def test_pagination(self):
        pages = [StringIO('{"data":[{"results":[{"amount":{"value":0.1,"currency":"usd"}}]}],"has_more":true,"next_page":"p2"}'),
                 StringIO('{"data":[{"results":[{"amount":{"value":0.2,"currency":"usd"}}]}],"has_more":false}')]
        with patch.object(usage, 'urlopen', side_effect=pages) as fetch:
            self.assertEqual(usage.costs(NOW.replace(day=1), NOW, 'test'), Decimal('0.3'))
        self.assertIn('page=p2', fetch.call_args[0][0].full_url)

    def test_missing_key(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(usage, 'costs') as fetch:
            self.assertIn('configure the OPENAI_ADMIN_KEY', usage.report(NOW, ''))
        fetch.assert_not_called()


if __name__ == '__main__':
    unittest.main()
