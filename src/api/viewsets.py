from rest_framework import viewsets, mixins
from django_filters import rest_framework as django_filters, FilterSet
from django.shortcuts import get_object_or_404
from django.http import Http404
from datetime import datetime
from api import serializers, exceptions
from core import models


class CallRecordFilter(FilterSet):

    class Meta:
        model = models.CallRecord
        fields = ['call_id', 'record_type', 'source']


class CallRecordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = models.CallRecord.objects.all()
    serializer_class = serializers.CallRecordSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
    )
    filter_class = CallRecordFilter


class BillRetrieveViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = models.Bill.objects.all()
    serializer_class = serializers.BillSerializer
    lookup_field = 'telephone'

    def get_object(self):
        period = self.request.GET.get('period', None)
        default_period = datetime.today()
        default_period = default_period.replace(day=1)

        if period:
            try:
                period = datetime.strptime(period, '%Y-%m')
                return get_object_or_404(
                    models.Bill,
                    telephone=self.kwargs['telephone'],
                    period=period
                )
            except ValueError:
                raise exceptions.InvalidPeriodFormat()
        else:
            bills = models.Bill.objects.filter(
                telephone=self.kwargs['telephone'],
                period__lt=default_period.date()
            ).order_by('-period')
            bill = bills.first()
            if bill:
                return bill
            else:
                raise Http404()
