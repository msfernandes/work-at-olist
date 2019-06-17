from django.urls import reverse
from rest_framework.test import APITestCase
from datetime import datetime
from core import models


class BillRetrieveViewSetTestCase(APITestCase):

    def test_bill_not_found(self):
        url = reverse('bill-detail', kwargs={'telephone': '99999999999'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_return_last_closed_bill(self):
        period = datetime.today()
        period = period.replace(day=1, month=period.month - 1)
        self.bill = models.Bill.objects.create(
            telephone='99999999999',
            period=period
        )

        url = reverse('bill-detail', kwargs={'telephone': '99999999999'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_specific_period(self):
        period = datetime.today()
        period = period.replace(day=1, month=period.month - 2)
        self.bill = models.Bill.objects.create(
            telephone='99999999999',
            period=period
        )

        url = reverse('bill-detail', kwargs={'telephone': '99999999999'})
        response = self.client.get(
            url + '?period=' + period.strftime('%Y-%m')
        )
        self.assertEqual(response.status_code, 200)

    def test_period_not_found(self):
        url = reverse('bill-detail', kwargs={'telephone': '99999999999'})
        response = self.client.get(url + '?period=2019-01')
        self.assertEqual(response.status_code, 404)

    def test_invalid_period_format(self):
        url = reverse('bill-detail', kwargs={'telephone': '99999999999'})
        response = self.client.get(url + '?period=209-1')
        self.assertEqual(response.status_code, 400)
