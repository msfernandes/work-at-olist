from rest_framework import viewsets
from django_filters import rest_framework as django_filters, FilterSet
from api import serializers
from core import models


class CallRecordFilter(FilterSet):

    class Meta:
        model = models.CallRecord
        fields = ['call_id', 'record_type', 'source']


class CallRecordViewSet(viewsets.ModelViewSet):

    queryset = models.CallRecord.objects.all()
    serializer_class = serializers.CallRecordSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
    )
    filter_class = CallRecordFilter
