from django.test import TestCase
from django.db.models import signals
from datetime import datetime, timezone
from core.signals import process_call_records
from core import models


class SignalsTestCase(TestCase):

    def setUp(self):
        signals.post_save.disconnect(
            sender=models.CallRecord,
            dispatch_uid='process_records'
        )

    def test_call_record_updated(self):
        timestamp = datetime(2019, 1, 1, 0, 0, tzinfo=timezone.utc)
        record = models.CallRecord.objects.create(
            call_id=1,
            record_type=models.CallRecord.START,
            timestamp=timestamp,
            source='9999999999',
            destination='99999999999',
        )

        process_call_records(models.CallRecord, record, False)
        self.assertEqual(models.BillRecord.objects.count(), 0)
        self.assertEqual(models.Bill.objects.count(), 0)

    def test_first_call_record(self):
        timestamp = datetime(2019, 1, 1, 0, 0, tzinfo=timezone.utc)
        record = models.CallRecord.objects.create(
            call_id=1,
            record_type=models.CallRecord.START,
            timestamp=timestamp,
            source='9999999999',
            destination='99999999999',
        )

        process_call_records(models.CallRecord, record, True)
        self.assertEqual(models.BillRecord.objects.count(), 0)
        self.assertEqual(models.Bill.objects.count(), 0)

    def test_second_call_record(self):
        timestamp = datetime(2019, 1, 1, 0, 0, tzinfo=timezone.utc)
        models.CallRecord.objects.create(
            call_id=1,
            record_type=models.CallRecord.START,
            timestamp=timestamp,
            source='9999999999',
            destination='99999999999',
        )

        end_timestamp = datetime(2019, 1, 1, 0, 1, tzinfo=timezone.utc)
        record = models.CallRecord.objects.create(
            call_id=1,
            record_type=models.CallRecord.END,
            timestamp=end_timestamp,
        )

        process_call_records(models.CallRecord, record, True)
        self.assertEqual(models.BillRecord.objects.count(), 1)
        self.assertEqual(models.Bill.objects.count(), 1)

    def test_second_call_record_inverted_order(self):
        timestamp = datetime(2019, 1, 1, 0, 1, tzinfo=timezone.utc)
        models.CallRecord.objects.create(
            call_id=1,
            record_type=models.CallRecord.END,
            timestamp=timestamp,
        )

        start_timestamp = datetime(2019, 1, 1, 0, 1, tzinfo=timezone.utc)
        record = models.CallRecord.objects.create(
            call_id=1,
            record_type=models.CallRecord.START,
            timestamp=start_timestamp,
            source='9999999999',
            destination='99999999999',
        )

        process_call_records(models.CallRecord, record, True)
        self.assertEqual(models.BillRecord.objects.count(), 1)
        self.assertEqual(models.Bill.objects.count(), 1)
