from django.test import TestCase
from datetime import datetime
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
