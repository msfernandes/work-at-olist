from rest_framework.serializers import ModelSerializer
from core import models


class CallRecordSerializer(ModelSerializer):

    class Meta:
        model = models.CallRecord
        fields = (
            'id',
            'call_id',
            'record_type',
            'timestamp',
            'source',
            'destination',
        )


class BillRecordSerializer(ModelSerializer):

    class Meta:
        model = models.BillRecord
        fields = (
            'destination',
            'start_date',
            'start_time',
            'duration',
            'price',
        )


class BillSerializer(ModelSerializer):

    class Meta:
        model = models.Bill
        fields = (
            'telephone',
            'period',
        )
