from django.test import TestCase
from datetime import datetime, date, time
from core import models


class CallRecordTestCase(TestCase):

    def test_str(self):
        timestamp = datetime(2019, 1, 1, 0, 0)
        record = models.CallRecord.objects.create(
            call_id=1,
            record_type=models.CallRecord.START,
            timestamp=timestamp,
            source='9999999999',
            destination='99999999999',
        )

        self.assertEqual(
            record.__str__(),
            'Call 1 - start <2019-01-01 00:00:00>'
        )


class BillRecordTestCase(TestCase):

    def setUp(self):
        period = datetime(2019, 1, 1,)
        self.bill = models.Bill.objects.create(
            telephone='9999999999',
            period=period
        )

    def test_str(self):
        record = models.BillRecord.objects.create(
            bill=self.bill,
            destination='99888888888',
            start_date=date(2019, 1, 1),
            start_time=time(0, 0),
            duration=60,
            price=1.75
        )

        self.assertEqual(
            record.__str__(),
            'Record from bill 1 - 60s - price: 1.75'
        )


class BillTestCase(TestCase):

    def test_str(self):
        period = datetime(2019, 1, 1,)
        bill = models.Bill.objects.create(
            telephone='9999999999',
            period=period
        )

        self.assertEqual(
            bill.__str__(),
            'Bill 1 from 9999999999 - 01-2019'
        )
