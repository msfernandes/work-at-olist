from rest_framework import serializers
from core import models


class CallRecordSerializer(serializers.ModelSerializer):

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


class BillRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BillRecord
        fields = (
            'destination',
            'start_date',
            'start_time',
            'duration',
            'price',
        )


class BillSerializer(serializers.ModelSerializer):
    records = BillRecordSerializer(many=True, read_only=True)

    class Meta:
        model = models.Bill
        fields = (
            'telephone',
            'period',
            'records'
        )
