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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        minutes, seconds = divmod(data['duration'], 60)
        hours, minutes = divmod(minutes, 60)
        data['duration'] = '{}h{}m{}s'.format(hours, minutes, seconds)
        return data


class BillSerializer(serializers.ModelSerializer):
    records = BillRecordSerializer(many=True, read_only=True)

    class Meta:
        model = models.Bill
        fields = (
            'telephone',
            'period',
            'records'
        )
