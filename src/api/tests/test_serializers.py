from django.test import TestCase
from datetime import datetime, date, time
from api import serializers
from core import models


class BillRecordSerializerTestCase(TestCase):

    def test_duration_representation(self):
        period = datetime(2019, 1, 1,)
        bill = models.Bill.objects.create(
            telephone='9999999999',
            period=period
        )
        record = models.BillRecord.objects.create(
            bill=bill,
            destination='99888888888',
            start_date=date(2019, 1, 1),
            start_time=time(0, 0),
            duration=60,
            price=1.75
        )
        serializer = serializers.BillRecordSerializer(record)

        self.assertEqual(serializer.data['duration'], '0h1m0s')

        record = models.BillRecord.objects.create(
            bill=bill,
            destination='99888888888',
            start_date=date(2019, 1, 1),
            start_time=time(0, 0),
            duration=4493,
            price=1.75
        )
        serializer = serializers.BillRecordSerializer(record)

        self.assertEqual(serializer.data['duration'], '1h14m53s')


class BillSerializerTestCase(TestCase):

    def test_period_representation(self):
        period = datetime(2019, 1, 1)
        self.bill = models.Bill.objects.create(
            telephone='9999999999',
            period=period.date()
        )
        serializer = serializers.BillSerializer(self.bill)
        self.assertEqual(serializer.data['period'], '2019-01')
