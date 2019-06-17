from django.test import TestCase
from datetime import datetime, timezone
from core import pricing


class PricingTestCase(TestCase):

    def test_start_time_smaller_than_end_time(self):
        start_timestamp = datetime(2019, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 0, 5, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.start, start_timestamp)

    def test_start_time_greater_than_end_time(self):
        start_timestamp = datetime(2019, 1, 1, 0, 5, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.start, end_timestamp)

    def test_call_duration(self):
        start_timestamp = datetime(2019, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 0, 5, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.call_duration(), 60 * 5)

        start_timestamp = datetime(2019, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.call_duration(), 0)

        start_timestamp = datetime(2019, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 0, 0, 1, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.call_duration(), 1)

    def test_check_standard_timestamp_tariff(self):
        timestamp = datetime(2019, 1, 1, 6, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(pricing.Pricing.check_tariff(timestamp), 'standard')

        timestamp = datetime(2019, 1, 1, 15, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(pricing.Pricing.check_tariff(timestamp), 'standard')

        timestamp = datetime(2019, 1, 1, 21, 59, 0, tzinfo=timezone.utc)
        self.assertEqual(pricing.Pricing.check_tariff(timestamp), 'standard')

        timestamp = datetime(2019, 1, 1, 22, 0, 0, tzinfo=timezone.utc)
        self.assertNotEqual(
            pricing.Pricing.check_tariff(timestamp),
            'standard'
        )

    def test_check_reduced_timestamp_tariff(self):
        timestamp = datetime(2019, 1, 1, 22, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(pricing.Pricing.check_tariff(timestamp), 'reduced')

        timestamp = datetime(2019, 1, 1, 4, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(pricing.Pricing.check_tariff(timestamp), 'reduced')

        timestamp = datetime(2019, 1, 1, 5, 59, 0, tzinfo=timezone.utc)
        self.assertEqual(pricing.Pricing.check_tariff(timestamp), 'reduced')

        timestamp = datetime(2019, 1, 1, 6, 0, 0, tzinfo=timezone.utc)
        self.assertNotEqual(
            pricing.Pricing.check_tariff(timestamp),
            'reduced'
        )

    def test_standard_start_tariff_duration(self):
        start_timestamp = datetime(2019, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 0, 5, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.start_tariff_duration('standard'), 0)

        start_timestamp = datetime(2019, 1, 1, 21, 50, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 22, 10, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.start_tariff_duration('standard'), 10 * 60)

    def test_reduced_start_tariff_duration(self):
        start_timestamp = datetime(2019, 1, 1, 6, 0, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 6, 5, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.start_tariff_duration('reduced'), 0)

        start_timestamp = datetime(2019, 1, 1, 5, 50, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 6, 10, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.start_tariff_duration('reduced'), 10 * 60)

    def test_duration_by_tariff_only_standard(self):
        start_timestamp = datetime(2019, 1, 1, 6, 0, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 6, 1, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.duration_by_tariff(),
                         {'standard': 60, 'reduced': 0})

        start_timestamp = datetime(2019, 1, 1, 21, 58, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 21, 59, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.duration_by_tariff(),
                         {'standard': 60, 'reduced': 0})

    def test_duration_by_tariff_only_reduced(self):
        start_timestamp = datetime(2019, 1, 1, 22, 0, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 22, 1, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.duration_by_tariff(),
                         {'standard': 0, 'reduced': 60})

        start_timestamp = datetime(2019, 1, 1, 5, 58, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 5, 59, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.duration_by_tariff(),
                         {'standard': 0, 'reduced': 60})

    def test_duration_by_tariff_mixed_tariffs(self):
        start_timestamp = datetime(2019, 1, 1, 5, 50, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 6, 10, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.duration_by_tariff(),
                         {'standard': 600, 'reduced': 600})

        start_timestamp = datetime(2019, 1, 1, 21, 55, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 22, 5, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.duration_by_tariff(),
                         {'standard': 5 * 60, 'reduced': 5 * 60})

    def test_call_price(self):
        start_timestamp = datetime(2019, 1, 1, 5, 50, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 6, 10, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.call_price(), round(0.36 + (10 * 0.09), 2))

        start_timestamp = datetime(2019, 1, 1, 5, 50, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 5, 55, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.call_price(), 0.36)

        start_timestamp = datetime(2019, 1, 1, 6, 50, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2019, 1, 1, 7, 10, 0, tzinfo=timezone.utc)
        price = pricing.Pricing(start_timestamp, end_timestamp)
        self.assertEqual(price.call_price(), round(0.36 + (20 * 0.09), 2))
